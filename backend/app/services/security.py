"""Account lockout (SCW-SEC-005): 5 failed logins in a row lock an account for 15 minutes."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.user import User

MAX_FAILED_LOGINS = 5
LOCK_DURATION = timedelta(minutes=15)


def _utc(value: datetime) -> datetime:
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def ensure_not_locked(user: User, now: datetime | None = None) -> None:
    """Refuse to log in while the account is locked, even with the right password."""
    now = now or datetime.now(timezone.utc)
    if user.locked_until and _utc(user.locked_until) > now:
        minutes = max(1, int((_utc(user.locked_until) - now).total_seconds() // 60) + 1)
        raise ApiError(
            403,
            "ACCOUNT_LOCKED",
            f"Too many failed logins. Try again in about {minutes} minute(s).",
        )


def record_failed_login(db: Session, user: User, now: datetime | None = None) -> bool:
    """Count a failed login; returns True when this failure locks the account."""
    now = now or datetime.now(timezone.utc)
    user.failed_login_attempts = (user.failed_login_attempts or 0) + 1
    locked = user.failed_login_attempts >= MAX_FAILED_LOGINS
    if locked:
        user.locked_until = now + LOCK_DURATION
        user.failed_login_attempts = 0
    db.commit()
    return locked


def record_successful_login(db: Session, user: User) -> None:
    """A good login resets the counter."""
    if user.failed_login_attempts or user.locked_until:
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()
