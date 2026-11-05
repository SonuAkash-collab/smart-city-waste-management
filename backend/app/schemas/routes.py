"""Pydantic schemas for routes (SAD 4.3, Route Service)."""

import datetime as dt
from typing import Literal

from pydantic import Field

from app.models.collection_request import WasteType
from app.models.route import RouteStatus, StopStatus, StopType
from app.models.vehicle import VehicleStatus
from app.schemas.base import CamelModel, UtcDateTime


class GenerateRoutes(CamelModel):
    date: dt.date


class StopOut(CamelModel):
    id: int
    sequence: int
    stop_type: StopType
    status: StopStatus
    latitude: float
    longitude: float
    load_after_kg: float | None = None
    distance_km: float | None = None
    completed_at: UtcDateTime | None = None
    request_id: int | None = None
    address: str | None = None
    waste_type: WasteType | None = None
    quantity_kg: float | None = None
    facility_id: int | None = None
    facility_name: str | None = None


class RouteOut(CamelModel):
    id: int
    date: dt.date
    status: RouteStatus
    vehicle_id: int
    vehicle_registration: str
    vehicle_capacity_kg: float
    vehicle_status: VehicleStatus
    driver_id: int | None = None
    driver_name: str | None = None
    total_distance_km: float | None = None
    stops: list[StopOut] = Field(default_factory=list)


class UnassignedOut(CamelModel):
    request_id: int
    reason: str


class AlertOut(CamelModel):
    vehicle_id: int
    load_kg: float
    waste_types: list[str]
    message: str


class GenerateResult(CamelModel):
    date: dt.date
    routes: list[RouteOut]
    unassigned: list[UnassignedOut]
    alerts: list[AlertOut]
    message: str


class StopUpdate(CamelModel):
    """Driver records the outcome of a stop (SCW-F-044)."""

    status: Literal["COLLECTED", "MISSED"]


class StopUpdated(CamelModel):
    route_id: int
    stop_id: int
    request_id: int | None
    status: StopStatus
    request_status: str | None
    route_status: RouteStatus
    vehicle_load_kg: float
