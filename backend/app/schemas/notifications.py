"""Pydantic schemas for notifications."""

from app.schemas.base import CamelModel, UtcDateTime


class NotificationOut(CamelModel):
    id: int
    message: str
    is_read: bool
    created_at: UtcDateTime


class NotificationList(CamelModel):
    items: list[NotificationOut]
    unread: int
