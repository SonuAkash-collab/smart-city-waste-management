"""Admin dashboard counts (SCW-F-051)."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.collection_request import CollectionRequest, Priority, RequestStatus
from app.models.vehicle import Vehicle, VehicleStatus
from app.services.facilities import describe, list_facilities
from app.services.requests import escalate_waiting_requests


def _counts(db: Session, column, values, *filters) -> dict[str, int]:
    rows = dict(db.execute(select(column, func.count()).where(*filters).group_by(column)).all())
    return {value.value: rows.get(value, 0) for value in values}


def summary(db: Session) -> dict:
    escalate_waiting_requests(db)
    return {
        "requests_by_status": _counts(db, CollectionRequest.status, RequestStatus),
        "pending_by_priority": _counts(
            db, CollectionRequest.priority, Priority, CollectionRequest.status == RequestStatus.SUBMITTED
        ),
        "vehicles_by_status": _counts(db, Vehicle.status, VehicleStatus),
        "facilities": [describe(db, f) for f in list_facilities(db)],
    }
