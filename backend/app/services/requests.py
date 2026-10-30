"""Business logic for collection requests (SCW-F-010 to SCW-F-014)."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.collection_request import CollectionRequest, Priority, RequestStatus, WasteType

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
