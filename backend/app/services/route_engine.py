"""Greedy route engine (SCW-F-040, SCW-F-041, SCW-F-042).

This module is pure Python: it takes plain data in and returns a plan out.
It does not touch the database or the API, so it is easy to test and fast
enough for 200 requests and 20 vehicles (SCW-NF-001).

Rules
-----
* Only the vehicles passed in are used; the caller passes AVAILABLE ones.
* A vehicle only collects waste types listed in its ``waste_types``.
* Vehicles take turns picking their next stop, so the work is spread over
  the fleet. Each pick is the highest-priority request first (HIGH, MEDIUM,
  LOW) and then the nearest one to the vehicle's current position.
* The planned load never goes above the vehicle's capacity.
* When the next stop would overflow a vehicle, it detours to the nearest
  facility that accepts every waste type on board and has enough remaining
  capacity, unloads, and carries on. If no facility qualifies, that route
  stops there and an admin alert is raised.
* At the end of a route a loaded vehicle goes to the nearest suitable
  facility to unload.
* Requests that no vehicle can take are returned in ``unassigned`` with a
  reason, and stay APPROVED for the next run.
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


def nearest_facility(
    facilities: list[FacilityInput],
    remaining: dict[int, float],
    waste_types: set[str],
    load_kg: float,
    latitude: float,
    longitude: float,
) -> FacilityInput | None:
    """Nearest facility that accepts every waste type on board and has room (SCW-F-032)."""
    suitable = [
        f
        for f in facilities
        if waste_types.issubset(f.accepted_waste_types) and remaining[f.id] >= load_kg
    ]
    if not suitable:
        return None
    return min(
        suitable,
        key=lambda f: (distance_km(latitude, longitude, f.latitude, f.longitude), f.id),
    )


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
        self.stopped = False

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

    def unload(self, facilities, remaining, alerts: list[AdminAlert]) -> bool:
        facility = nearest_facility(
            facilities, remaining, self.on_board, self.load, self.latitude, self.longitude
        )
        if facility is None:
            types = tuple(sorted(self.on_board))
            alerts.append(
                AdminAlert(
                    vehicle_id=self.vehicle.id,
                    load_kg=round(self.load, 3),
                    waste_types=types,
                    message=(
                        f"Vehicle {self.vehicle.id} carries {self.load:.0f} kg "
                        f"({', '.join(types)}) and no facility can take it. "
                        "Its route stops here until an admin acts."
                    ),
                )
            )
            self.active = False
            self.stopped = True
            return False
        remaining[facility.id] -= self.load
        self.load = 0.0
        self.on_board.clear()
        self.add_stop(FACILITY, facility.latitude, facility.longitude, facility_id=facility.id)
        return True


def _reason(request: RequestInput, vehicles: list[VehicleInput]) -> str:
    takes_type = [v for v in vehicles if request.waste_type in v.waste_types]
    if not takes_type:
        return NO_COMPATIBLE_VEHICLE
    if all(request.quantity_kg > v.capacity_kg for v in takes_type):
        return TOO_LARGE
    return NO_CAPACITY


def plan_routes(
    requests: list[RequestInput],
    vehicles: list[VehicleInput],
    facilities: list[FacilityInput] | None = None,
) -> RoutePlan:
    """Build one route per vehicle that has work."""
    plan = RoutePlan()
    facilities = list(facilities or [])
    remaining = {f.id: f.remaining_capacity_kg for f in facilities}
    pending = sorted(requests, key=lambda r: r.id)
    states = [_VehicleState(v) for v in sorted(vehicles, key=lambda v: v.id)]

    # Vehicles take turns: each turn a vehicle collects one stop or unloads.
    while any(state.active for state in states):
        for state in states:
            if not state.active:
                continue
            candidates = [r for r in pending if can_carry(state.vehicle, r)]
            nxt = pick_next(candidates, state.latitude, state.longitude)
            if nxt is None:
                state.active = False
                continue
            if state.load + nxt.quantity_kg > state.vehicle.capacity_kg:
                # The next stop would overflow the vehicle: unload first (SCW-F-042).
                state.unload(facilities, remaining, plan.alerts)
                continue
            pending.remove(nxt)
            state.collect(nxt)

    for state in states:
        # A route that ends with waste on board finishes at a facility.
        if state.load > 0 and not state.stopped and state.route.stops:
            state.unload(facilities, remaining, plan.alerts)
        if state.route.stops:
            plan.routes.append(state.route)

    plan.unassigned = [UnassignedRequest(r.id, _reason(r, vehicles)) for r in pending]
    return plan
