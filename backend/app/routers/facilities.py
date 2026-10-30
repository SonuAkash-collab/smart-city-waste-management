from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import User, UserRole
from app.schemas.facilities import (
    FacilityCreate,
    FacilityRead,
    FacilityUpdate,
    IntakeCreate,
    IntakeRead,
)
from app.services import facilities as facility_service

router = APIRouter(prefix="/facilities", tags=["facilities"])

admin_only = [Depends(require_roles(UserRole.ADMIN))]
admin_or_operator = [Depends(require_roles(UserRole.ADMIN, UserRole.OPERATOR))]


@router.post("", response_model=FacilityRead, status_code=status.HTTP_201_CREATED, dependencies=admin_only)
def add_facility(data: FacilityCreate, db: Session = Depends(get_db)):
    """Admin registers a disposal facility (SCW-F-030)."""
    facility = facility_service.create_facility(db, data)
    return facility_service.describe(db, facility)


@router.get("", response_model=list[FacilityRead], dependencies=admin_or_operator)
def list_facilities(db: Session = Depends(get_db)):
    """Facilities with today's remaining capacity."""
    return [facility_service.describe(db, f) for f in facility_service.list_facilities(db)]


@router.get("/{facility_id}", response_model=FacilityRead, dependencies=admin_or_operator)
def get_facility(facility_id: int, db: Session = Depends(get_db)):
    return facility_service.describe(db, facility_service.get_facility(db, facility_id))


@router.patch("/{facility_id}", response_model=FacilityRead, dependencies=admin_only)
def edit_facility(facility_id: int, data: FacilityUpdate, db: Session = Depends(get_db)):
    facility = facility_service.update_facility(db, facility_id, data)
    return facility_service.describe(db, facility)


@router.post("/{facility_id}/intakes", response_model=IntakeRead, status_code=status.HTTP_201_CREATED)
def record_intake(
    facility_id: int,
    data: IntakeCreate,
    db: Session = Depends(get_db),
    operator: User = Depends(require_roles(UserRole.OPERATOR)),
):
    """Operator records an incoming delivery (SCW-F-031)."""
    intake, remaining = facility_service.record_intake(db, facility_id, operator, data)
    return _intake_out(intake, remaining)


@router.get("/{facility_id}/intakes", response_model=list[IntakeRead], dependencies=admin_or_operator)
def list_intakes(
    facility_id: int,
    on_date: date | None = Query(default=None, alias="date"),
    db: Session = Depends(get_db),
):
    """Deliveries recorded at a facility on one day (today by default)."""
    facility = facility_service.get_facility(db, facility_id)
    remaining = facility_service.remaining_capacity(db, facility, on_date)
    return [_intake_out(i, remaining) for i in facility_service.list_intakes(db, facility_id, on_date)]


def _intake_out(intake, remaining: float) -> dict:
    return {
        "id": intake.id,
        "facility_id": intake.facility_id,
        "vehicle_id": intake.vehicle_id,
        "operator_id": intake.operator_id,
        "waste_type": intake.waste_type,
        "weight_kg": intake.weight_kg,
        "recorded_at": intake.recorded_at,
        "remaining_capacity_kg": remaining,
    }
