"""Password hashing (SCW-SEC-001) and JWT access tokens (SCW-SEC-002)."""

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt

from app.core import config
from app.core.errors import ApiError

MAX_PASSWORD_BYTES = 72  # bcrypt only reads the first 72 bytes


def hash_password(password: str) -> str:
    """Return a bcrypt hash; the plain password is never stored."""
    salt = bcrypt.gensalt(rounds=config.BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Check a password against its stored bcrypt hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(user_id: int, role: str, now: datetime | None = None) -> str:
    """Issue a signed JWT that carries the user's id and role."""
    issued_at = now or datetime.now(timezone.utc)
    expires_at = issued_at + timedelta(minutes=config.ACCESS_TOKEN_MINUTES)
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Return the token claims or raise a 401 error."""
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
    except ExpiredSignatureError as exc:
        raise ApiError(401, "TOKEN_EXPIRED", "Your session has expired. Please log in again.") from exc
    except JWTError as exc:
        raise ApiError(401, "INVALID_TOKEN", "The access token is not valid.") from exc
