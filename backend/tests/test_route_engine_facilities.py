"""Tests for facility detours and admin alerts (TC-RT-02, TC-RT-04, TC-FAC-01 step 9-10)."""

from app.services.route_engine import (
    COLLECTION,
    FACILITY,
    NO_CAPACITY,
    FacilityInput,
    plan_routes,
)

from tests.test_route_engine import DEPOT, req, truck


def plant(id, lat_offset, accepts=("MIXED",), remaining=10_000.0):
    return FacilityInput(
        id=id,
        latitude=DEPOT[0] + lat_offset,
        longitude=DEPOT[1],
        accepted_waste_types=tuple(accepts),
        remaining_capacity_kg=remaining,
    )


def kinds(route):
    return [(s.stop_type, s.request_id or s.facility_id) for s in route.stops]


def test_full_vehicle_detours_to_nearest_facility_and_continues():
    requests = [req(1, 0.010, qty=60), req(2, 0.020, qty=60), req(3, 0.030, qty=30)]
    plan = plan_routes(requests, [truck(capacity=100)], [plant(9, 0.015)])
    route = plan.routes[0]
    assert kinds(route) == [
        (COLLECTION, 1),
        (FACILITY, 9),
        (COLLECTION, 2),
        (COLLECTION, 3),
        (FACILITY, 9),  # unloads at the end of the route
    ]
    assert all(stop.load_after_kg <= 100 for stop in route.stops)
    assert route.stops[1].load_after_kg == 0
    assert plan.unassigned == []
    assert plan.alerts == []


def test_detour_skips_facilities_that_are_full_or_wrong_type():
    requests = [req(1, 0.010, qty=80), req(2, 0.012, qty=80)]
    facilities = [
        plant(7, 0.011, accepts=("GARDEN",)),       # nearest, wrong waste type
        plant(8, 0.013, remaining=50),              # near, not enough room
        plant(9, 0.040),                            # far, suitable
    ]
    plan = plan_routes(requests, [truck(capacity=100)], facilities)
    detours = [s.facility_id for s in plan.routes[0].stops if s.stop_type == FACILITY]
    assert detours[0] == 9


def test_facility_must_accept_every_waste_type_on_board():
    requests = [
        req(1, 0.010, qty=40, waste="MIXED", priority="HIGH"),
        req(2, 0.011, qty=40, waste="GARDEN", priority="HIGH"),
        req(3, 0.012, qty=40, waste="MIXED"),
    ]
    facilities = [plant(5, 0.013, accepts=("MIXED",)), plant(6, 0.050, accepts=("MIXED", "GARDEN"))]
    plan = plan_routes(requests, [truck(capacity=100)], facilities)
    detours = [s.facility_id for s in plan.routes[0].stops if s.stop_type == FACILITY]
    assert detours[0] == 6


def test_facility_capacity_is_shared_between_vehicles():
    requests = [req(i, 0.001 * i, qty=100) for i in range(1, 5)]
    facilities = [plant(9, 0.010, remaining=250)]
    plan = plan_routes(requests, [truck(1, capacity=100), truck(2, capacity=100)], facilities)
    unloaded = 0.0
    for route in plan.routes:
        for previous, stop in zip(route.stops, route.stops[1:]):
            if stop.stop_type == FACILITY:
                unloaded += previous.load_after_kg
    assert unloaded <= 250
    assert len(plan.alerts) == 2  # both trucks end full with no room left


def test_no_suitable_facility_stops_route_and_alerts_admin():
    # TC-RT-04: the vehicle is full and every facility is too small.
    requests = [req(1, 0.010, qty=90), req(2, 0.020, qty=90)]
    plan = plan_routes(requests, [truck(id=4, capacity=100)], [plant(9, 0.015, remaining=10)])
    route = plan.routes[0]
    assert kinds(route) == [(COLLECTION, 1)]
    assert route.stops[-1].load_after_kg <= 100
    assert len(plan.alerts) == 1
    alert = plan.alerts[0]
    assert alert.vehicle_id == 4
    assert alert.load_kg == 90
    assert "no facility can take it" in alert.message
    assert [(u.request_id, u.reason) for u in plan.unassigned] == [(2, NO_CAPACITY)]


def test_end_of_route_without_facility_raises_alert():
    plan = plan_routes([req(1, 0.01, qty=10)], [truck()], [])
    assert len(plan.alerts) == 1
    assert plan.alerts[0].load_kg == 10
