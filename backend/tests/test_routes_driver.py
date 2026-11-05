"""Tests for viewing routes and driver stop updates (TC-RT-03, SCW-F-021, SCW-F-023)."""

import pytest

from app.models.collection_request import CollectionRequest, RequestStatus
from app.models.notification import Notification
from app.models.user import UserRole
from app.models.vehicle import VehicleStatus

from tests.test_routes_api import DAY, add_facility, add_request, add_vehicle, generate


@pytest.fixture
def planned(client, admin_headers, db_session, citizen, driver):
    """One route with three collection stops and a final facility stop."""
    vehicle = add_vehicle(db_session, driver)
    add_facility(db_session)
    requests = [add_request(db_session, citizen, offset) for offset in (0.01, 0.02, 0.03)]
    route = generate(client, admin_headers).json()["routes"][0]
    return {"route": route, "vehicle": vehicle, "requests": requests}


def stop_url(route, stop):
    return f"/api/v1/routes/{route['id']}/stops/{stop['id']}"


def test_driver_sees_assigned_route_in_order(client, driver_headers, planned):
    routes = client.get("/api/v1/routes/assigned", headers=driver_headers).json()
    assert len(routes) == 1
    stops = routes[0]["stops"]
    assert [s["sequence"] for s in stops] == list(range(1, len(stops) + 1))
    assert all(s["latitude"] and s["longitude"] for s in stops)
    assert stops[0]["address"] and stops[0]["wasteType"] == "MIXED"


def test_driver_lists_and_opens_own_route(client, driver_headers, planned):
    listed = client.get(f"/api/v1/routes?date={DAY}", headers=driver_headers).json()
    assert [r["id"] for r in listed] == [planned["route"]["id"]]
    one = client.get(f"/api/v1/routes/{planned['route']['id']}", headers=driver_headers)
    assert one.status_code == 200


def test_admin_lists_routes_by_date(client, admin_headers, planned):
    assert len(client.get(f"/api/v1/routes?date={DAY}", headers=admin_headers).json()) == 1
    assert client.get("/api/v1/routes?date=2030-01-01", headers=admin_headers).json() == []


def test_other_driver_cannot_see_or_update(client, make_user, headers_for, planned):
    other = headers_for(make_user(UserRole.DRIVER))
    route = planned["route"]
    assert client.get(f"/api/v1/routes/{route['id']}", headers=other).status_code == 403
    assert client.get("/api/v1/routes/assigned", headers=other).json() == []
    response = client.patch(stop_url(route, route["stops"][0]), json={"status": "COLLECTED"}, headers=other)
    assert response.status_code == 403


def test_citizen_cannot_view_routes(client, citizen_headers, planned):
    assert client.get(f"/api/v1/routes?date={DAY}", headers=citizen_headers).status_code == 403


def test_mark_collected_and_missed(client, driver_headers, citizen_headers, planned, db_session):
    route = planned["route"]
    first, second, third = route["stops"][:3]

    done = client.patch(stop_url(route, first), json={"status": "COLLECTED"}, headers=driver_headers)
    assert done.status_code == 200
    assert done.json()["requestStatus"] == "COLLECTED"
    assert done.json()["routeStatus"] == "IN_PROGRESS"
    assert done.json()["vehicleLoadKg"] == 20

    missed = client.patch(stop_url(route, second), json={"status": "MISSED"}, headers=driver_headers)
    assert missed.json()["requestStatus"] == "MISSED"

    # The citizen sees the new statuses (TC-RT-03 step 6) and the third is untouched (step 7).
    status_of = lambda stop: client.get(f"/api/v1/requests/{stop['requestId']}", headers=citizen_headers).json()["status"]  # noqa: E731
    assert status_of(first) == "COLLECTED"
    assert status_of(second) == "MISSED"
    assert status_of(third) == "SCHEDULED"

    reopened = client.get(f"/api/v1/routes/{route['id']}", headers=driver_headers).json()
    assert [s["status"] for s in reopened["stops"][:3]] == ["COLLECTED", "MISSED", "PENDING"]


def test_each_update_notifies_the_owner(client, driver_headers, planned, citizen, db_session):
    route = planned["route"]
    before = db_session.query(Notification).filter_by(user_id=citizen.id).count()
    client.patch(stop_url(route, route["stops"][0]), json={"status": "COLLECTED"}, headers=driver_headers)
    assert db_session.query(Notification).filter_by(user_id=citizen.id).count() == before + 1


def test_stop_cannot_be_updated_twice(client, driver_headers, planned):
    route = planned["route"]
    client.patch(stop_url(route, route["stops"][0]), json={"status": "COLLECTED"}, headers=driver_headers)
    again = client.patch(stop_url(route, route["stops"][0]), json={"status": "MISSED"}, headers=driver_headers)
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "STOP_ALREADY_DONE"


def test_unknown_stop_and_route(client, driver_headers, planned):
    route = planned["route"]
    assert client.patch(f"/api/v1/routes/{route['id']}/stops/9999", json={"status": "MISSED"}, headers=driver_headers).status_code == 404
    assert client.get("/api/v1/routes/9999", headers=driver_headers).status_code == 404


def test_invalid_outcome_rejected(client, driver_headers, planned):
    route = planned["route"]
    response = client.patch(stop_url(route, route["stops"][0]), json={"status": "DONE"}, headers=driver_headers)
    assert response.status_code == 422


def test_finishing_route_frees_vehicle_and_unloads(client, driver_headers, planned, db_session):
    route = planned["route"]
    for stop in route["stops"]:
        response = client.patch(stop_url(route, stop), json={"status": "COLLECTED"}, headers=driver_headers)
        assert response.status_code == 200
    assert response.json()["routeStatus"] == "COMPLETED"
    assert response.json()["vehicleLoadKg"] == 0  # last stop is the facility
    vehicle = planned["vehicle"]
    db_session.refresh(vehicle)
    assert vehicle.status == VehicleStatus.AVAILABLE
    assert client.get("/api/v1/routes/assigned", headers=driver_headers).json() == []
    completed = client.patch(stop_url(route, route["stops"][0]), json={"status": "MISSED"}, headers=driver_headers)
    assert completed.status_code == 409


def test_vehicle_in_maintenance_stays_there(client, driver_headers, planned, db_session):
    vehicle = planned["vehicle"]
    vehicle.status = VehicleStatus.MAINTENANCE
    db_session.commit()
    route = planned["route"]
    for stop in route["stops"]:
        client.patch(stop_url(route, stop), json={"status": "MISSED"}, headers=driver_headers)
    db_session.refresh(vehicle)
    assert vehicle.status == VehicleStatus.MAINTENANCE


def test_overloaded_vehicle_is_refused(client, driver_headers, planned, db_session):
    vehicle = planned["vehicle"]
    vehicle.current_load_kg = vehicle.capacity_kg  # already full
    db_session.commit()
    route = planned["route"]
    response = client.patch(stop_url(route, route["stops"][0]), json={"status": "COLLECTED"}, headers=driver_headers)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "VEHICLE_FULL"
    request = db_session.get(CollectionRequest, route["stops"][0]["requestId"])
    assert request.status == RequestStatus.SCHEDULED
