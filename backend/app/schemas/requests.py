"""Pydantic schemas for requests (SAD 4.3, Request Service)."""

from typing import Literal

from pydantic import Field, field_validator

from app.models.collection_request import Priority, RequestStatus, WasteType
from app.schemas.base import CamelModel, UtcDateTime

MAX_PHOTO_CHARS = 7_000_000  # about 5 MB of image data in base64


class RequestCreate(CamelModel):
    """A Citizen's new collection request (SCW-F-010).

    Latitude and longitude come from the map pin, or from geocoding the
    address in the web app. They are optional here so that a missing location
    gets the agreed ``LOCATION_REQUIRED`` error instead of a generic one.
    """

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    address: str | None = Field(default=None, max_length=255)
    waste_type: WasteType
    estimated_quantity_kg: float = Field(gt=0, le=10_000)
    photo: str | None = Field(default=None, max_length=MAX_PHOTO_CHARS)

    @field_validator("address")
    @classmethod
    def strip_address(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class RequestCreated(CamelModel):
    id: int
    status: RequestStatus
    priority: Priority
    created_at: UtcDateTime


class RequestOut(CamelModel):
    """The full request object returned to its owner or an Admin."""

    id: int
    citizen_id: int
    latitude: float
    longitude: float
    address: str | None
    waste_type: WasteType
    estimated_quantity_kg: float
    has_photo: bool
    status: RequestStatus
    priority: Priority
    priority_overridden: bool = False
    reason: str | None
    created_at: UtcDateTime
    updated_at: UtcDateTime


class RequestDetail(RequestOut):
    photo: str | None = None


class RequestPage(CamelModel):
    items: list[RequestOut]
    page: int
    size: int
    total: int


class StatusUpdate(CamelModel):
    """Admin decision on a request (SCW-F-014) with an optional priority override (SCW-F-011)."""

    status: Literal["APPROVED", "REJECTED"]
    priority: Priority | None = None
    reason: str | None = Field(default=None, max_length=255)


class StatusUpdated(CamelModel):
    id: int
    status: RequestStatus
    priority: Priority
    updated_at: UtcDateTime


class CancelResult(CamelModel):
    id: int
    status: RequestStatus
