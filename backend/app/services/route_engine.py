"""Greedy route engine (SCW-F-040, SCW-F-041, SCW-F-042).

This module is pure Python: it takes plain data in and returns a plan out.
It does not touch the database or the API, so it is easy to test and fast
enough for 200 requests and 20 vehicles (SCW-NF-001).
"""

from dataclasses import dataclass, field

from app.services.geo import haversine_distance

PRIORITY_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}

COLLECTION = "COLLECTION"
FACILITY = "FACILITY"

NO_COMPATIBLE_VEHICLE = "NO_COMPATIBLE_VEHICLE"
TOO_LARGE = "TOO_LARGE"
NO_CAPACITY = "NO_CAPACITY"


@dataclass(frozen=True)
class RequestInput:
    id: int
    latitude: float
    longitude: float
    waste_type: str
    quantity_kg: float
    priority: str


@dataclass(frozen=True)
class VehicleInput:
    id: int
    capacity_kg: float
    waste_types: tuple[str, ...]
    depot_latitude: float
    depot_longitude: float
    current_load_kg: float = 0.0


@dataclass(frozen=True)
class FacilityInput:
    id: int
    latitude: float
    longitude: float
    accepted_waste_types: tuple[str, ...]
    remaining_capacity_kg: float


@dataclass
class PlannedStop:
    sequence: int
    stop_type: str
    latitude: float
    longitude: float
    load_after_kg: float
    distance_km: float
    request_id: int | None = None
    facility_id: int | None = None


@dataclass
class PlannedRoute:
    vehicle_id: int
    stops: list[PlannedStop] = field(default_factory=list)

    @property
    def total_distance_km(self) -> float:
        return round(sum(stop.distance_km for stop in self.stops), 3)


@dataclass
class UnassignedRequest:
    request_id: int
    reason: str


@dataclass
class AdminAlert:
    vehicle_id: int
    load_kg: float
    waste_types: tuple[str, ...]
    message: str


@dataclass
class RoutePlan:
    routes: list[PlannedRoute] = field(default_factory=list)
    unassigned: list[UnassignedRequest] = field(default_factory=list)
    alerts: list[AdminAlert] = field(default_factory=list)


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return haversine_distance(lat1, lon1, lat2, lon2)


def priority_rank(priority: str) -> int:
    return PRIORITY_RANK.get(priority, len(PRIORITY_RANK))
