"""Pydantic schemas for the audit log."""

from app.schemas.base import CamelModel, UtcDateTime


class AuditEntry(CamelModel):
    id: int
    user_id: int | None
    actor_name: str | None = None
    action: str
    entity_type: str | None
    entity_id: int | None
    details: str | None
    created_at: UtcDateTime
