"""Audit log of Admin actions (SCW-SEC-006).

A middleware records every successful change an Admin makes through the API
(approve or reject, route generation, account changes, vehicle and facility
edits) with the actor, the action, the affected record and the time.
"""

import inspect
import re

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.errors import ApiError
from app.core.security import decode_access_token
from app.db import get_db
from app.models.audit_log import AuditLog

CHANGING_METHODS = {"POST", "PATCH", "PUT", "DELETE"}

# (method, path pattern, action name, entity type)
ACTIONS = [
    ("PATCH", r"^/api/v1/requests/(\d+)/status$", "REQUEST_DECIDED", "request"),
    ("POST", r"^/api/v1/routes/generate$", "ROUTES_GENERATED", "route"),
    ("POST", r"^/api/v1/users$", "ACCOUNT_CREATED", "user"),
    ("PATCH", r"^/api/v1/users/(\d+)/status$", "ACCOUNT_STATUS_CHANGED", "user"),
    ("POST", r"^/api/v1/vehicles/?$", "VEHICLE_CREATED", "vehicle"),
    ("PATCH", r"^/api/v1/vehicles/(\d+)$", "VEHICLE_UPDATED", "vehicle"),
    ("PATCH", r"^/api/v1/vehicles/(\d+)/driver$", "DRIVER_ASSIGNED", "vehicle"),
    ("POST", r"^/api/v1/facilities$", "FACILITY_CREATED", "facility"),
    ("PATCH", r"^/api/v1/facilities/(\d+)$", "FACILITY_UPDATED", "facility"),
]


def describe_action(method: str, path: str) -> tuple[str, str | None, int | None]:
    for want, pattern, action, entity in ACTIONS:
        found = re.match(pattern, path)
        if want == method and found:
            entity_id = int(found.group(1)) if found.groups() else None
            return action, entity, entity_id
    return f"{method} {path}", None, None


def _admin_id(request: Request) -> int | None:
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    try:
        claims = decode_access_token(header[7:])
    except ApiError:
        return None
    return int(claims["sub"]) if claims.get("role") == "ADMIN" else None


def _open_session(request: Request):
    """Use the same session provider as the endpoints (tests override it)."""
    provider = request.app.dependency_overrides.get(get_db, get_db)
    result = provider()
    if inspect.isgenerator(result):
        return next(result), result
    return result, None


def write_entry(db: Session, user_id: int, action: str, entity_type, entity_id, details: str) -> AuditLog:
    entry = AuditLog(
        user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id, details=details
    )
    db.add(entry)
    db.commit()
    return entry


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.method in CHANGING_METHODS and response.status_code < 400:
            admin_id = _admin_id(request)
            if admin_id is not None:
                action, entity, entity_id = describe_action(request.method, request.url.path)
                db, generator = _open_session(request)
                try:
                    write_entry(
                        db, admin_id, action, entity, entity_id,
                        f"{request.method} {request.url.path} -> {response.status_code}",
                    )
                finally:
                    if generator is not None:
                        generator.close()
        return response


def list_entries(db: Session, limit: int = 100) -> list[AuditLog]:
    return list(db.scalars(select(AuditLog).order_by(AuditLog.id.desc()).limit(limit)).all())
