from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import UserRole
from app.schemas.dashboard import DashboardOut
from app.services.dashboard import summary

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(require_roles(UserRole.ADMIN))])


@router.get("", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db)):
    """Requests by status, pending by priority, vehicles by status, facility capacity (SCW-F-051)."""
    return summary(db)
