"""Business logic for disposal facilities (SCW-F-030 to SCW-F-032)."""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.facility import Facility, FacilityIntake
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.facilities import FacilityCreate, FacilityUpdate, IntakeCreate
from app.services.route_engine import FacilityInput
from app.services.vehicles import unload


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


def record_intake(
    db: Session, facility_id: int, operator: User, data: IntakeCreate
) -> tuple[FacilityIntake, float]:
    """Operator records a delivery; returns the intake and the remaining capacity (SCW-F-031).

    The facility row is locked while the check and insert run, so two
    deliveries at the same time cannot go over the daily capacity.
    """
    facility = db.scalar(select(Facility).where(Facility.id == facility_id).with_for_update())
    if facility is None:
        raise ApiError(404, "FACILITY_NOT_FOUND", "Facility not found.")
    if db.get(Vehicle, data.vehicle_id) is None:
        raise ApiError(422, "UNKNOWN_VEHICLE", "No registered vehicle has this id.")
    if data.waste_type.value not in facility.accepted_waste_types:
        raise ApiError(
            422,
            "WASTE_TYPE_NOT_ACCEPTED",
            f"{facility.name} does not accept {data.waste_type.value} waste.",
        )
    now = datetime.now(timezone.utc)
    remaining = remaining_capacity(db, facility, now.date())
    if data.weight_kg > remaining:
        db.rollback()
        raise ApiError(
            409,
            "CAPACITY_EXCEEDED",
            f"Only {remaining:.0f} kg of capacity is left today.",
        )
    intake = FacilityIntake(
        facility_id=facility.id,
        vehicle_id=data.vehicle_id,
        operator_id=operator.id,
        waste_type=data.waste_type,
        weight_kg=data.weight_kg,
        recorded_at=now,
    )
    db.add(intake)
    db.commit()
    db.refresh(intake)
    # The delivered waste leaves the vehicle (SCW-F-023).
    unload(db, data.vehicle_id, data.weight_kg)
    return intake, round(remaining - data.weight_kg, 3)


def list_intakes(db: Session, facility_id: int, day: date | None = None) -> list[FacilityIntake]:
    get_facility(db, facility_id)
    start = datetime.combine(day or today(), time.min, tzinfo=timezone.utc)
    return list(
        db.scalars(
            select(FacilityIntake)
            .where(
                FacilityIntake.facility_id == facility_id,
                FacilityIntake.recorded_at >= _db_time(db, start),
                FacilityIntake.recorded_at < _db_time(db, start + timedelta(days=1)),
            )
            .order_by(FacilityIntake.recorded_at)
        ).all()
    )


def suitable_facilities(
    db: Session, waste_types: set[str], load_kg: float, day: date | None = None
) -> list[Facility]:
    """Facilities that accept every given waste type and have room for the load (SCW-F-032).

    Full facilities, facilities that do not take one of the waste types, and
    facilities with less remaining capacity than the load are left out.
    """
    day = day or today()
    return [
        facility
        for facility in list_facilities(db)
        if waste_types.issubset(facility.accepted_waste_types)
        and remaining_capacity(db, facility, day) >= load_kg
        and remaining_capacity(db, facility, day) > 0
    ]


def routing_facilities(db: Session, day: date | None = None) -> list[FacilityInput]:
    """Facilities with capacity left on ``day``, in the form the route engine reads."""
    day = day or today()
    inputs = []
    for facility in list_facilities(db):
        remaining = remaining_capacity(db, facility, day)
        if remaining <= 0:
            continue
        inputs.append(
            FacilityInput(
                id=facility.id,
                latitude=facility.latitude,
                longitude=facility.longitude,
                accepted_waste_types=tuple(facility.accepted_waste_types),
                remaining_capacity_kg=remaining,
            )
        )
    return inputs
