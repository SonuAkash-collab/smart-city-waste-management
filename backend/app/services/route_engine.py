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


def can_carry(vehicle: VehicleInput, request: RequestInput) -> bool:
    """True when the vehicle takes this waste type and the load fits when empty."""
    return request.waste_type in vehicle.waste_types and request.quantity_kg <= vehicle.capacity_kg


def pick_next(
    candidates: list[RequestInput], latitude: float, longitude: float
) -> RequestInput | None:
    """Highest priority first, then the nearest request; ties go to the lower id."""
    if not candidates:
        return None
    best_rank = min(priority_rank(r.priority) for r in candidates)
    tier = [r for r in candidates if priority_rank(r.priority) == best_rank]
    return min(
        tier,
        key=lambda r: (distance_km(latitude, longitude, r.latitude, r.longitude), r.id),
    )


def order_stops(
    requests: list[RequestInput], latitude: float, longitude: float
) -> list[RequestInput]:
    """Visiting order for one vehicle with room for everything (SCW-F-041)."""
    remaining = list(requests)
    ordered: list[RequestInput] = []
    while remaining:
        nxt = pick_next(remaining, latitude, longitude)
        ordered.append(nxt)
        remaining.remove(nxt)
        latitude, longitude = nxt.latitude, nxt.longitude
    return ordered


class _VehicleState:
    """A vehicle's position, load and route while the plan is being built."""

    def __init__(self, vehicle: VehicleInput):
        self.vehicle = vehicle
        self.route = PlannedRoute(vehicle_id=vehicle.id)
        self.latitude = vehicle.depot_latitude
        self.longitude = vehicle.depot_longitude
        self.load = vehicle.current_load_kg
        self.on_board: set[str] = set()
        self.active = True

    def add_stop(self, stop_type, latitude, longitude, request_id=None, facility_id=None):
        leg = distance_km(self.latitude, self.longitude, latitude, longitude)
        self.route.stops.append(
            PlannedStop(
                sequence=len(self.route.stops) + 1,
                stop_type=stop_type,
                latitude=latitude,
                longitude=longitude,
                load_after_kg=round(self.load, 3),
                distance_km=round(leg, 3),
                request_id=request_id,
                facility_id=facility_id,
            )
        )
        self.latitude, self.longitude = latitude, longitude

    def collect(self, request: RequestInput) -> None:
        self.load += request.quantity_kg
        self.on_board.add(request.waste_type)
        self.add_stop(COLLECTION, request.latitude, request.longitude, request_id=request.id)


def _reason(request: RequestInput, vehicles: list[VehicleInput]) -> str:
    takes_type = [v for v in vehicles if request.waste_type in v.waste_types]
    if not takes_type:
        return NO_COMPATIBLE_VEHICLE
    if all(request.quantity_kg > v.capacity_kg for v in takes_type):
        return TOO_LARGE
    return NO_CAPACITY


def plan_routes(requests: list[RequestInput], vehicles: list[VehicleInput]) -> RoutePlan:
    """Build one route per vehicle that has work.

    Vehicles take turns picking their next stop so the work is spread over the
    fleet. A vehicle whose next stop would overflow it ends its route.
    """
    plan = RoutePlan()
    pending = sorted(requests, key=lambda r: r.id)
    states = [_VehicleState(v) for v in sorted(vehicles, key=lambda v: v.id)]

    while any(state.active for state in states):
        for state in states:
            if not state.active:
                continue
            candidates = [r for r in pending if can_carry(state.vehicle, r)]
            nxt = pick_next(candidates, state.latitude, state.longitude)
            if nxt is None or state.load + nxt.quantity_kg > state.vehicle.capacity_kg:
                state.active = False
                continue
            pending.remove(nxt)
            state.collect(nxt)

    plan.routes = [state.route for state in states if state.route.stops]
    plan.unassigned = [UnassignedRequest(r.id, _reason(r, vehicles)) for r in pending]
    return plan
