"""Pydantic schemas for dashboard."""

from app.schemas.base import CamelModel
from app.schemas.facilities import FacilityRead


class DashboardOut(CamelModel):
    requests_by_status: dict[str, int]
    pending_by_priority: dict[str, int]
    vehicles_by_status: dict[str, int]
    facilities: list[FacilityRead]
