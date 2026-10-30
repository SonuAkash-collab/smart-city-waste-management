from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import UserRole
from app.schemas.auth import UserOut
from app.schemas.users import StaffCreate, UserStatusUpdate
from app.services import users as user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_staff_account(data: StaffCreate, db: Session = Depends(get_db)):
    """Admin creates a Driver or Operator account."""
    return user_service.create_staff(db, data)


@router.get("", response_model=list[UserOut])
def list_accounts(role: UserRole | None = None, db: Session = Depends(get_db)):
    """Admin lists accounts, optionally filtered by role."""
    return user_service.list_users(db, role)


@router.patch("/{user_id}/status", response_model=UserOut)
def change_account_status(user_id: int, data: UserStatusUpdate, db: Session = Depends(get_db)):
    """Admin activates or deactivates a non-Admin account."""
    return user_service.set_active(db, user_id, data.is_active)
