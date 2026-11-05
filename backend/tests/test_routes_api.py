"""Tests for POST /routes/generate (TC-RT-01, TC-RT-02, TC-RT-04, TC-VEH-01 steps 6-10)."""

from datetime import date

import pytest

from app.models.collection_request import CollectionRequest, Priority, RequestStatus, WasteType
from app.models.facility import Facility
from app.models.notification import Notification
from app.models.route import Route
from app.models.user import UserRole
from app.models.vehicle import Vehicle, VehicleStatus

DAY = "2026-11-02"
DEPOT = (12.9300, 77.5400)


def add_vehicle(db, driver, reg="KA01AB1234", capacity=1000, types=("MIXED", "GARDEN", "HAZARDOUS"),
                status=VehicleStatus.AVAILABLE, depot=DEPOT):
    vehicle = Vehicle(
        registration_number=reg,
        capacity_kg=capacity,
        current_load_kg=0,
        waste_types=list(types),
        depot_latitude=depot[0],
        depot_longitude=depot[1],
        status=status,
        driver_id=driver.id if driver else None,
    )
    db.add(vehicle)
    db.commit()
    return vehicle


def add_facility(db, name="Plant", offset=0.02, types=("MIXED", "GARDEN", "HAZARDOUS"), capacity=10_000):
    facility = Facility(
        name=name,
        latitude=DEPOT[0] - offset,
        longitude=DEPOT[1],
        accepted_waste_types=list(types),
        daily_capacity_kg=capacity,
    )
    db.add(facility)
    db.commit()
    return facility


def add_request(db, citizen, offset, waste="MIXED", kg=20, status=RequestStatus.APPROVED, priority=None):
    request = CollectionRequest(
        citizen_id=citizen.id,
        latitude=DEPOT[0] + offset,
        longitude=DEPOT[1],
        address=f"{offset} north",
        waste_type=WasteType(waste),
        estimated_quantity_kg=kg,
        status=status,
        priority=priority or {"HAZARDOUS": Priority.HIGH, "MIXED": Priority.MEDIUM, "GARDEN": Priority.LOW}[waste],
    )
    db.add(request)
    db.commit()
    return request


def generate(client, headers, day=DAY):
    return client.post("/api/v1/routes/generate", json={"date": day}, headers=headers)


def collection_order(route):
    return [s["requestId"] for s in route["stops"] if s["stopType"] == "COLLECTION"]


def test_generate_orders_by_priority_then_distance(client, admin_headers, db_session, citizen, driver):
    # TC-RT-01: four approved requests, two with equal priority, and one unapproved.
    add_vehicle(db_session, driver)
    add_facility(db_session)
    far_medium = add_request(db_session, citizen, 0.030, "MIXED")
    near_medium = add_request(db_session, citizen, 0.010, "MIXED")
    high = add_request(db_session, citizen, 0.050, "HAZARDOUS")
    low = add_request(db_session, citizen, 0.002, "GARDEN")
    unapproved = add_request(db_session, citizen, 0.005, "MIXED", status=RequestStatus.SUBMITTED)

    response = generate(client, admin_headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body["routes"]) == 1
    route = body["routes"][0]
    assert collection_order(route) == [high.id, far_medium.id, near_medium.id, low.id]
    assert unapproved.id not in collection_order(route)
    assert route["date"] == DAY
    assert route["status"] == "PLANNED"
    assert route["driverName"] == driver.full_name
    assert route["totalDistanceKm"] > 0


def test_planned_requests_become_scheduled_and_owner_is_told(client, admin_headers, db_session, citizen, driver):
    add_vehicle(db_session, driver)
    add_facility(db_session)
    request = add_request(db_session, citizen, 0.01)
    generate(client, admin_headers)
    db_session.refresh(request)
    assert request.status == RequestStatus.SCHEDULED
    messages = [n.message for n in db_session.query(Notification).filter_by(user_id=citizen.id)]
    assert any("SCHEDULED" in m for m in messages)


def test_vehicle_goes_on_route(client, admin_headers, db_session, citizen, driver):
    vehicle = add_vehicle(db_session, driver)
    add_request(db_session, citizen, 0.01)
    generate(client, admin_headers)
    db_session.refresh(vehicle)
    assert vehicle.status == VehicleStatus.ON_ROUTE


def test_capacity_respected_with_facility_detour(client, admin_headers, db_session, citizen, driver):
    # TC-RT-02: combined load is above capacity, so the route visits the facility.
    add_vehicle(db_session, driver, capacity=100)
    plant = add_facility(db_session, offset=-0.015)
    for offset in (0.01, 0.02, 0.03):
        add_request(db_session, citizen, offset, kg=60)
    route = generate(client, admin_headers).json()["routes"][0]
    assert all(s["loadAfterKg"] <= 100 for s in route["stops"])
    kinds = [s["stopType"] for s in route["stops"]]
    assert kinds.count("COLLECTION") == 3
    assert kinds[1] == "FACILITY"
    assert route["stops"][1]["facilityName"] == plant.name


def test_no_facility_stops_route_and_alerts_admin(client, admin, admin_headers, db_session, citizen, driver):
    # TC-RT-04: no facility can take the load.
    add_vehicle(db_session, driver, capacity=100)
    add_facility(db_session, capacity=10)
    first = add_request(db_session, citizen, 0.01, kg=90)
    second = add_request(db_session, citizen, 0.02, kg=90)
    body = generate(client, admin_headers).json()
    route = body["routes"][0]
    assert collection_order(route) == [first.id]
    assert all(s["loadAfterKg"] <= 100 for s in route["stops"])
    assert body["alerts"] and "no facility can take it" in body["alerts"][0]["message"]
    assert body["unassigned"] == [{"requestId": second.id, "reason": "NO_CAPACITY"}]
    db_session.refresh(second)
    assert second.status == RequestStatus.APPROVED
    admin_messages = [n.message for n in db_session.query(Notification).filter_by(user_id=admin.id)]
    assert any("Route alert" in m for m in admin_messages)
    assert any(f"#{second.id}" in m for m in admin_messages)


def test_maintenance_and_driverless_vehicles_not_used(client, admin_headers, db_session, citizen, make_user):
    # TC-VEH-01 steps 9-10 and SCW-F-021.
    add_vehicle(db_session, make_user(UserRole.DRIVER), reg="KA01MAINT", status=VehicleStatus.MAINTENANCE)
    add_vehicle(db_session, None, reg="KA01NODRV")
    add_request(db_session, citizen, 0.01)
    body = generate(client, admin_headers).json()
    assert body["routes"] == []
    assert body["unassigned"][0]["reason"] == "NO_COMPATIBLE_VEHICLE"
    assert "No routes planned" in body["message"]


def test_vehicle_on_route_not_given_a_second_route(client, admin_headers, db_session, citizen, driver):
    # TC-VEH-01 step 7: a vehicle with an active route is not planned again.
    add_vehicle(db_session, driver)
    add_facility(db_session)
    add_request(db_session, citizen, 0.01)
    generate(client, admin_headers)
    add_request(db_session, citizen, 0.02)
    body = generate(client, admin_headers, day="2026-11-03").json()
    assert body["routes"] == []


def test_second_run_for_same_day_conflicts(client, admin_headers, db_session, citizen, driver):
    add_vehicle(db_session, driver)
    add_request(db_session, citizen, 0.01)
    generate(client, admin_headers)
    response = generate(client, admin_headers)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ROUTES_EXIST"
    assert db_session.query(Route).count() == 1


def test_nothing_to_plan(client, admin_headers):
    body = generate(client, admin_headers).json()
    assert body["routes"] == [] and body["unassigned"] == []


@pytest.mark.parametrize("who", ["citizen_headers", "driver_headers", "operator_headers"])
def test_only_admin_generates(client, request, db_session, who):
    # TC-AUTH-02 steps 2-4: 403 and no route created.
    response = generate(client, request.getfixturevalue(who))
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"
    assert db_session.query(Route).count() == 0


def test_bad_date_rejected(client, admin_headers):
    assert client.post("/api/v1/routes/generate", json={"date": "tomorrow"}, headers=admin_headers).status_code == 422


def test_route_date_is_the_requested_one(client, admin_headers, db_session, citizen, driver):
    add_vehicle(db_session, driver)
    add_request(db_session, citizen, 0.01)
    generate(client, admin_headers, day="2026-12-01")
    assert db_session.query(Route).one().route_date == date(2026, 12, 1)
