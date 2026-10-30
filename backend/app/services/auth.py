"""Business logic for auth: registration and login (SCW-F-001)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import config
from app.core.errors import ApiError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.strip().lower()))


def register_citizen(db: Session, data: RegisterRequest) -> User:
    """Create a Citizen account; the email must be unique."""
    if get_user_by_email(db, data.email) is not None:
        raise ApiError(409, "EMAIL_TAKEN", "An account with this email already exists.")
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=UserRole.CITIZEN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    """Return the user for valid credentials or raise 401.

    The same error is used for an unknown email and a wrong password so the
    response does not reveal which emails are registered.
    """
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise ApiError(401, "INVALID_CREDENTIALS", "Email or password is incorrect.")
    if not user.is_active:
        raise ApiError(401, "ACCOUNT_DEACTIVATED", "This account has been deactivated.")
    return user


def issue_token(user: User) -> dict:
    return {
        "access_token": create_access_token(user.id, user.role.value),
        "token_type": "bearer",
        "expires_in": config.ACCESS_TOKEN_MINUTES * 60,
        "user": user,
    }
