"""Business logic for users: Admin account management (SCW-F-003)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.schemas.users import StaffCreate
from app.services.auth import get_user_by_email


def create_staff(db: Session, data: StaffCreate) -> User:
    """Create a Driver or Operator account."""
    if get_user_by_email(db, data.email) is not None:
        raise ApiError(409, "EMAIL_TAKEN", "An account with this email already exists.")
    user = User(
        email=data.email,
        full_name=data.full_name,
        role=UserRole(data.role),
        hashed_password=hash_password(data.temporary_password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, role: UserRole | None = None) -> list[User]:
    query = select(User).order_by(User.id)
    if role is not None:
        query = query.where(User.role == role)
    return list(db.scalars(query).all())


def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise ApiError(404, "USER_NOT_FOUND", "User not found.")
    return user


def set_active(db: Session, user_id: int, is_active: bool) -> User:
    """Activate or deactivate a non-Admin account."""
    user = get_user(db, user_id)
    if user.role == UserRole.ADMIN:
        raise ApiError(409, "ADMIN_ACCOUNT_LOCKED", "Admin accounts cannot be deactivated here.")
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user
