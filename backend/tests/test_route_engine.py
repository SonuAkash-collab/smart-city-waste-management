"""Tests for the greedy route engine: ordering and capacity (TC-RT-01, TC-RT-02)."""

from app.services.route_engine import (
    COLLECTION,
    NO_CAPACITY,
    NO_COMPATIBLE_VEHICLE,
    TOO_LARGE,
    RequestInput,
    VehicleInput,
    order_stops,
    pick_next,
    plan_routes,
)

DEPOT = (12.9350, 77.5350)  # near PES University, Bengaluru


def req(id, lat_offset, priority="MEDIUM", qty=10.0, waste="MIXED"):
    """A request placed ``lat_offset`` degrees north of the depot."""
    return RequestInput(
        id=id,
        latitude=DEPOT[0] + lat_offset,
        longitude=DEPOT[1],
        waste_type=waste,
        quantity_kg=qty,
        priority=priority,
    )


def truck(id=1, capacity=1000.0, waste=("MIXED", "HAZARDOUS", "GARDEN"), depot=DEPOT):
    return VehicleInput(
        id=id,
        capacity_kg=capacity,
        waste_types=tuple(waste),
        depot_latitude=depot[0],
        depot_longitude=depot[1],
    )


def collected_ids(route):
    return [s.request_id for s in route.stops if s.stop_type == COLLECTION]


def test_empty_input_gives_empty_plan():
    plan = plan_routes([], [truck()])
    assert plan.routes == []
    assert plan.unassigned == []


def test_pick_next_prefers_priority_over_distance():
    near_low = req(1, 0.001, "LOW")
    far_high = req(2, 0.050, "HIGH")
    assert pick_next([near_low, far_high], *DEPOT).id == 2


def test_pick_next_breaks_equal_priority_by_distance():
    far = req(1, 0.020)
    near = req(2, 0.005)
    assert pick_next([far, near], *DEPOT).id == 2


def test_order_stops_priority_then_nearest():
    stops = [
        req(1, 0.030, "LOW"),
        req(2, 0.010, "MEDIUM"),
        req(3, 0.040, "HIGH"),
        req(4, 0.020, "HIGH"),
        req(5, 0.005, "MEDIUM"),
    ]
    ordered = [r.id for r in order_stops(stops, *DEPOT)]
    # HIGH first (nearest HIGH first), then MEDIUM nearest to the last stop, then LOW.
    assert ordered == [4, 3, 2, 5, 1]


def test_route_follows_priority_then_distance():
    # TC-RT-01: two equal-priority requests at different distances.
    plan = plan_routes(
        [req(1, 0.030, "MEDIUM"), req(2, 0.010, "MEDIUM"), req(3, 0.050, "HIGH"), req(4, 0.002, "LOW")],
        [truck()],
    )
    assert len(plan.routes) == 1
    assert collected_ids(plan.routes[0]) == [3, 1, 2, 4]
    assert plan.unassigned == []


def test_sequence_numbers_and_distance():
    plan = plan_routes([req(1, 0.01), req(2, 0.02)], [truck()])
    route = plan.routes[0]
    assert [s.sequence for s in route.stops][:2] == [1, 2]
    assert route.stops[0].distance_km > 1.0  # about 1.1 km north of the depot
    assert route.total_distance_km == round(sum(s.distance_km for s in route.stops), 3)


def test_load_never_exceeds_capacity():
    requests = [req(i, 0.001 * i, qty=30) for i in range(1, 11)]
    plan = plan_routes(requests, [truck(capacity=100)])
    for route in plan.routes:
        for stop in route.stops:
            assert stop.load_after_kg <= 100


def test_full_vehicle_without_facility_leaves_rest_unassigned():
    plan = plan_routes([req(1, 0.01, qty=60), req(2, 0.02, qty=50)], [truck(capacity=100)])
    assert collected_ids(plan.routes[0]) == [1]
    assert [(u.request_id, u.reason) for u in plan.unassigned] == [(2, NO_CAPACITY)]


def test_vehicle_only_takes_its_waste_types():
    plan = plan_routes(
        [req(1, 0.01, waste="MEDICAL"), req(2, 0.02, waste="MIXED")],
        [truck(waste=("MIXED",))],
    )
    assert collected_ids(plan.routes[0]) == [2]
    assert [(u.request_id, u.reason) for u in plan.unassigned] == [(1, NO_COMPATIBLE_VEHICLE)]


def test_request_bigger_than_any_vehicle():
    plan = plan_routes([req(1, 0.01, qty=5000)], [truck(capacity=1000)])
    assert plan.routes == []
    assert [(u.request_id, u.reason) for u in plan.unassigned] == [(1, TOO_LARGE)]


def test_no_vehicles_means_everything_unassigned():
    plan = plan_routes([req(1, 0.01)], [])
    assert plan.routes == []
    assert plan.unassigned[0].reason == NO_COMPATIBLE_VEHICLE


def test_work_is_spread_over_vehicles():
    north_depot = (DEPOT[0] + 0.10, DEPOT[1])
    requests = [req(1, 0.001), req(2, 0.002), req(3, 0.101), req(4, 0.102)]
    plan = plan_routes(requests, [truck(1), truck(2, depot=north_depot)])
    by_vehicle = {route.vehicle_id: collected_ids(route) for route in plan.routes}
    assert by_vehicle == {1: [1, 2], 2: [3, 4]}


def test_each_request_is_planned_once():
    requests = [req(i, 0.002 * i, priority=("HIGH", "MEDIUM", "LOW")[i % 3]) for i in range(1, 31)]
    plan = plan_routes(requests, [truck(1), truck(2), truck(3)])
    planned = [rid for route in plan.routes for rid in collected_ids(route)]
    assert sorted(planned) == list(range(1, 31))
