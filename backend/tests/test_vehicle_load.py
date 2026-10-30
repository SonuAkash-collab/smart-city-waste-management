"""Tests for vehicle load tracking (SCW-F-023) and Admin-only access (TC-VEH-02 step 6)."""

import pytest

from app.models.user import UserRole
from app.models.vehicle import Vehicle, VehicleStatus
from app.services.vehicles import VehicleOverloadError, add_load, unload


@pytest.fixture
def truck(db_session):
    vehicle = Vehicle(
        registration_number="KA05LD0001",
        capacity_kg=500,
        current_load_kg=0,
        waste_types=["MIXED"],
        depot_latitude=12.93,
        depot_longitude=77.53,
        status=VehicleStatus.AVAILABLE,
    )
    db_session.add(vehicle)
    db_session.commit()
    return vehicle


def test_each_collection_adds_to_the_load(db_session, truck):
    add_load(db_session, truck.id, 120)
    add_load(db_session, truck.id, 80.5)
    assert truck.current_load_kg == 200.5


def test_load_can_reach_but_not_pass_capacity(db_session, truck):
    add_load(db_session, truck.id, 500)
    with pytest.raises(VehicleOverloadError):
        add_load(db_session, truck.id, 1)
    assert truck.current_load_kg == 500


def test_negative_weight_rejected(db_session, truck):
    with pytest.raises(ValueError):
        add_load(db_session, truck.id, -1)


def test_unload_part_or_all(db_session, truck):
    add_load(db_session, truck.id, 300)
    unload(db_session, truck.id, 100)
    assert truck.current_load_kg == 200
    unload(db_session, truck.id, 999)
    assert truck.current_load_kg == 0
    add_load(db_session, truck.id, 50)
    unload(db_session, truck.id)
    assert truck.current_load_kg == 0


def test_load_shows_in_vehicle_details(client, admin_headers, db_session, truck):
    add_load(db_session, truck.id, 75)
    response = client.get(f"/api/v1/vehicles/{truck.id}", headers=admin_headers)
    assert response.json()["currentLoadKg"] == 75


@pytest.mark.parametrize("role", [UserRole.CITIZEN, UserRole.DRIVER, UserRole.OPERATOR])
def test_vehicle_endpoints_are_admin_only(client, make_user, headers_for, truck, role):
    headers = headers_for(make_user(role))
    assert client.get("/api/v1/vehicles/", headers=headers).status_code == 403
    response = client.patch(
        f"/api/v1/vehicles/{truck.id}/driver", json={"driverId": 1}, headers=headers
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_vehicle_endpoints_need_login(client, truck):
    assert client.get("/api/v1/vehicles/").status_code == 401
    assert client.post("/api/v1/vehicles/", json={}).status_code == 401
