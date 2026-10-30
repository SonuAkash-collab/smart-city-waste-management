"""Business logic for disposal facilities (SCW-F-030 to SCW-F-032)."""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.facility import Facility, FacilityIntake
from app.schemas.facilities import FacilityCreate, FacilityUpdate


def today() -> date:
    return datetime.now(timezone.utc).date()


def _db_time(db: Session, value: datetime) -> datetime:
    """SQLite keeps naive UTC datetimes; other databases keep the time zone."""
    return value.replace(tzinfo=None) if db.get_bind().dialect.name == "sqlite" else value


def used_on(db: Session, facility_id: int, day: date) -> float:
    """Total weight delivered to a facility on one day."""
    start = datetime.combine(day, time.min, tzinfo=timezone.utc)
    total = db.scalar(
        select(func.coalesce(func.sum(FacilityIntake.weight_kg), 0.0)).where(
            FacilityIntake.facility_id == facility_id,
            FacilityIntake.recorded_at >= _db_time(db, start),
            FacilityIntake.recorded_at < _db_time(db, start + timedelta(days=1)),
        )
    )
    return float(total or 0.0)


def remaining_capacity(db: Session, facility: Facility, day: date | None = None) -> float:
    """Daily capacity minus what was delivered that day, never below zero."""
    return max(0.0, facility.daily_capacity_kg - used_on(db, facility.id, day or today()))


def describe(db: Session, facility: Facility, day: date | None = None) -> dict:
    """Facility fields plus today's usage, for API responses and the dashboard."""
    used = used_on(db, facility.id, day or today())
    remaining = max(0.0, facility.daily_capacity_kg - used)
    return {
        "id": facility.id,
        "name": facility.name,
        "latitude": facility.latitude,
        "longitude": facility.longitude,
        "accepted_waste_types": list(facility.accepted_waste_types),
        "daily_capacity_kg": facility.daily_capacity_kg,
        "used_today_kg": round(used, 3),
        "remaining_capacity_kg": round(remaining, 3),
        "remaining_percent": round(100 * remaining / facility.daily_capacity_kg, 1),
    }


def get_facility(db: Session, facility_id: int) -> Facility:
    facility = db.get(Facility, facility_id)
    if facility is None:
        raise ApiError(404, "FACILITY_NOT_FOUND", "Facility not found.")
    return facility


def list_facilities(db: Session) -> list[Facility]:
    return list(db.scalars(select(Facility).order_by(Facility.id)).all())


def create_facility(db: Session, data: FacilityCreate) -> Facility:
    facility = Facility(
        name=data.name,
        latitude=data.latitude,
        longitude=data.longitude,
        accepted_waste_types=data.accepted_waste_types,
        daily_capacity_kg=data.daily_capacity_kg,
    )
    db.add(facility)
    db.commit()
    db.refresh(facility)
    return facility


def update_facility(db: Session, facility_id: int, data: FacilityUpdate) -> Facility:
    facility = get_facility(db, facility_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(facility, field, value)
    db.commit()
    db.refresh(facility)
    return facility
