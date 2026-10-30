"""Business logic for collection requests (SCW-F-010 to SCW-F-014)."""

import base64
import binascii
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.collection_request import CollectionRequest, Priority, RequestStatus, WasteType
from app.models.user import User, UserRole
from app.schemas.requests import RequestCreate, StatusUpdate
from app.services.notifications import notify

# SCW-F-011: priority from waste type.
PRIORITY_BY_WASTE_TYPE = {
    WasteType.HAZARDOUS: Priority.HIGH,
    WasteType.MEDICAL: Priority.HIGH,
    WasteType.E_WASTE: Priority.HIGH,
    WasteType.MIXED: Priority.MEDIUM,
    WasteType.RECYCLABLE: Priority.MEDIUM,
    WasteType.GARDEN: Priority.LOW,
    WasteType.BULKY: Priority.LOW,
}


def initial_priority(waste_type: WasteType) -> Priority:
    """Return the starting priority for a waste type."""
    return PRIORITY_BY_WASTE_TYPE[waste_type]


ESCALATION_AGE = timedelta(hours=48)
NEXT_LEVEL = {Priority.LOW: Priority.MEDIUM, Priority.MEDIUM: Priority.HIGH, Priority.HIGH: Priority.HIGH}
WAITING_STATUSES = (RequestStatus.SUBMITTED, RequestStatus.APPROVED)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(value: datetime) -> datetime:
    """SQLite gives back naive datetimes; they are stored in UTC."""
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def escalate_waiting_requests(db: Session, now: datetime | None = None) -> int:
    """Raise by one level the priority of requests waiting over 48 hours (SCW-F-011).

    Each request goes up once, HIGH stays HIGH, and a priority set by an Admin
    is never changed. Called before requests are read or routes are planned,
    so the stored priority is always current. Returns how many changed.
    """
    now = now or utcnow()
    waiting = db.scalars(
        select(CollectionRequest).where(
            CollectionRequest.status.in_(WAITING_STATUSES),
            CollectionRequest.priority_escalated.is_(False),
            CollectionRequest.priority_overridden.is_(False),
        )
    ).all()
    changed = 0
    for request in waiting:
        if now - as_utc(request.created_at) > ESCALATION_AGE:
            request.priority = NEXT_LEVEL[request.priority]
            request.priority_escalated = True
            changed += 1
    if changed:
        db.commit()
    return changed


def announce_status(db: Session, request: CollectionRequest) -> None:
    """Tell the owner about the request's current status (SCW-F-050)."""
    when = as_utc(request.updated_at or request.created_at or utcnow())
    notify(
        db,
        request.citizen_id,
        f"Request #{request.id}: status is now {request.status.value} "
        f"({when:%Y-%m-%d %H:%M} UTC).",
    )


def _check_photo(photo: str) -> None:
    data = photo.split(",", 1)[1] if photo.startswith("data:") else photo
    try:
        base64.b64decode(data, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ApiError(422, "INVALID_PHOTO", "The photo must be a base64-encoded image.") from exc


def create_request(db: Session, citizen: User, data: RequestCreate) -> CollectionRequest:
    """Store a new request with its starting priority (SCW-F-010, SCW-F-011)."""
    if data.latitude is None or data.longitude is None:
        raise ApiError(
            422,
            "LOCATION_REQUIRED",
            "Pin the location on the map or enter an address we can find.",
        )
    if data.photo:
        _check_photo(data.photo)
    now = utcnow()
    request = CollectionRequest(
        citizen_id=citizen.id,
        latitude=data.latitude,
        longitude=data.longitude,
        address=data.address,
        waste_type=data.waste_type,
        estimated_quantity_kg=data.estimated_quantity_kg,
        photo=data.photo,
        status=RequestStatus.SUBMITTED,
        priority=initial_priority(data.waste_type),
        created_at=now,
        updated_at=now,
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    announce_status(db, request)
    return request


def _db_time(db: Session, value: datetime) -> datetime:
    """SQLite keeps naive UTC datetimes; other databases keep the time zone."""
    return value.replace(tzinfo=None) if db.get_bind().dialect.name == "sqlite" else value


def list_requests(
    db: Session,
    user: User,
    status: RequestStatus | None = None,
    priority: Priority | None = None,
    waste_type: WasteType | None = None,
    on_date: date | None = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[CollectionRequest], int]:
    """Filter and page requests (SCW-F-014). Citizens only see their own."""
    escalate_waiting_requests(db)
    query = select(CollectionRequest)
    if user.role != UserRole.ADMIN:
        query = query.where(CollectionRequest.citizen_id == user.id)
    if status is not None:
        query = query.where(CollectionRequest.status == status)
    if priority is not None:
        query = query.where(CollectionRequest.priority == priority)
    if waste_type is not None:
        query = query.where(CollectionRequest.waste_type == waste_type)
    if on_date is not None:
        start = datetime.combine(on_date, time.min, tzinfo=timezone.utc)
        query = query.where(
            CollectionRequest.created_at >= _db_time(db, start),
            CollectionRequest.created_at < _db_time(db, start + timedelta(days=1)),
        )
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    items = db.scalars(
        query.order_by(CollectionRequest.created_at.desc(), CollectionRequest.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    return list(items), total


def get_request(db: Session, request_id: int) -> CollectionRequest:
    request = db.get(CollectionRequest, request_id)
    if request is None:
        raise ApiError(404, "REQUEST_NOT_FOUND", "Request not found.")
    return request


def get_request_for(db: Session, user: User, request_id: int) -> CollectionRequest:
    """Return a request to its owner or an Admin (SCW-F-012)."""
    escalate_waiting_requests(db)
    request = get_request(db, request_id)
    if user.role != UserRole.ADMIN and request.citizen_id != user.id:
        raise ApiError(403, "FORBIDDEN", "You can only view your own requests.")
    return request


# Which statuses an Admin decision may start from.
DECISION_ALLOWED_FROM = {
    RequestStatus.APPROVED: {RequestStatus.SUBMITTED, RequestStatus.APPROVED},
    RequestStatus.REJECTED: {RequestStatus.SUBMITTED, RequestStatus.APPROVED},
}


def decide(db: Session, request_id: int, data: StatusUpdate) -> CollectionRequest:
    """Admin approves or rejects a request and may override its priority (SCW-F-011, SCW-F-014)."""
    request = get_request(db, request_id)
    target = RequestStatus(data.status)
    if request.status not in DECISION_ALLOWED_FROM[target]:
        raise ApiError(
            409,
            "INVALID_STATUS_TRANSITION",
            f"A {request.status.value} request cannot be {target.value.lower()}.",
        )
    status_changed = request.status != target
    request.status = target
    if data.priority is not None:
        request.priority = data.priority
        request.priority_overridden = True
    if data.reason is not None:
        request.reason = data.reason
    request.updated_at = utcnow()
    db.commit()
    db.refresh(request)
    if status_changed:
        announce_status(db, request)
    return request
