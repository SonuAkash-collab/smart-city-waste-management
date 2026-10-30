"""Request dependencies for authentication and role checks.

Role checks run on the server for every protected endpoint (SCW-SEC-004).
Use them in a router like this::

    @router.post("/generate", dependencies=[Depends(require_roles(UserRole.ADMIN))])
    def generate(...): ...

or, when the endpoint needs the user object::

    def submit(user: User = Depends(require_roles(UserRole.CITIZEN))): ...
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.db import get_db
from app.models.user import User, UserRole

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Return the logged-in user or raise 401."""
    if credentials is None or not credentials.credentials:
        raise ApiError(401, "NOT_AUTHENTICATED", "Please log in to continue.")
    claims = decode_access_token(credentials.credentials)
    try:
        user_id = int(claims.get("sub", ""))
    except ValueError as exc:
        raise ApiError(401, "INVALID_TOKEN", "The access token is not valid.") from exc
    user = db.get(User, user_id)
    if user is None:
        raise ApiError(401, "INVALID_TOKEN", "The access token is not valid.")
    if not user.is_active:
        # Tokens of deactivated accounts stop working at once (SCW-F-003).
        raise ApiError(401, "ACCOUNT_DEACTIVATED", "This account has been deactivated.")
    return user


def require_roles(*roles: UserRole):
    """Allow only users whose role is one of ``roles``; others get 403.

    The role is read from the database, never from the token or the client,
    so changing data on the client cannot raise privileges.
    """

    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise ApiError(403, "FORBIDDEN", "You do not have permission to do this.")
        return user

    return checker
