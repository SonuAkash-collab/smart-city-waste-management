from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import UserRole
from app.schemas.facilities import FacilityCreate, FacilityRead, FacilityUpdate
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
