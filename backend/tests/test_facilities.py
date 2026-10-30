"""Tests for facilities: registration (TC-FAC-02) and intake (TC-FAC-01)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.models.facility import FacilityIntake
from app.models.vehicle import Vehicle, VehicleStatus
from app.services.facilities import routing_facilities, suitable_facilities, today


def facility_payload(**overrides):
    body = {
        "name": "Facility A, Bengaluru",
        "latitude": 12.95,
        "longitude": 77.62,
        "acceptedWasteTypes": ["MIXED", "GARDEN"],
        "dailyCapacityKg": 1000,
    }
    body.update(overrides)
    return body


@pytest.fixture
def facility(client, admin_headers):
    return client.post("/api/v1/facilities", json=facility_payload(), headers=admin_headers).json()


@pytest.fixture
def vehicle(db_session):
    truck = Vehicle(
        registration_number="KA01AB1234",
        capacity_kg=2000,
        current_load_kg=900,
        waste_types=["MIXED", "GARDEN"],
        depot_latitude=12.93,
        depot_longitude=77.53,
        status=VehicleStatus.AVAILABLE,
    )
    db_session.add(truck)
    db_session.commit()
    return truck


def intake(client, operator_headers, facility_id, vehicle_id, weight, waste="MIXED"):
    return client.post(
        f"/api/v1/facilities/{facility_id}/intakes",
        json={"vehicleId": vehicle_id, "wasteType": waste, "weightKg": weight},
        headers=operator_headers,
    )


# --- registration (TC-FAC-02) ------------------------------------------------


def test_register_and_read_facility(client, admin_headers):
    created = client.post("/api/v1/facilities", json=facility_payload(), headers=admin_headers)
    assert created.status_code == 201
    body = created.json()
    stored = client.get(f"/api/v1/facilities/{body['id']}", headers=admin_headers).json()
    assert stored["name"] == "Facility A, Bengaluru"
    assert stored["acceptedWasteTypes"] == ["MIXED", "GARDEN"]
    assert stored["dailyCapacityKg"] == 1000
    assert stored["remainingCapacityKg"] == 1000
    assert stored["remainingPercent"] == 100.0


@pytest.mark.parametrize(
    "change",
    [
        {"latitude": None},
        {"acceptedWasteTypes": []},
        {"acceptedWasteTypes": ["WET"]},
        {"dailyCapacityKg": 0},
        {"dailyCapacityKg": -100},
        {"name": "   "},
    ],
)
def test_invalid_facility_rejected(client, admin_headers, change):
    body = facility_payload(**change)
    body = {k: v for k, v in body.items() if v is not None}
    response = client.post("/api/v1/facilities", json=body, headers=admin_headers)
    assert response.status_code == 422


def test_citizen_cannot_register_facility(client, citizen_headers):
    response = client.post("/api/v1/facilities", json=facility_payload(), headers=citizen_headers)
    assert response.status_code == 403


def test_operator_can_list_but_not_edit(client, operator_headers, facility):
    assert client.get("/api/v1/facilities", headers=operator_headers).status_code == 200
    response = client.patch(
        f"/api/v1/facilities/{facility['id']}", json={"dailyCapacityKg": 10}, headers=operator_headers
    )
    assert response.status_code == 403


def test_admin_edits_facility(client, admin_headers, facility):
    response = client.patch(
        f"/api/v1/facilities/{facility['id']}",
        json={"dailyCapacityKg": 5000, "acceptedWasteTypes": ["recyclable"]},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["dailyCapacityKg"] == 5000
    assert response.json()["acceptedWasteTypes"] == ["RECYCLABLE"]


def test_edit_rejects_null(client, admin_headers, facility):
    response = client.patch(
        f"/api/v1/facilities/{facility['id']}", json={"name": None}, headers=admin_headers
    )
    assert response.status_code == 422


def test_unknown_facility(client, admin_headers):
    assert client.get("/api/v1/facilities/999", headers=admin_headers).status_code == 404


# --- intake (TC-FAC-01) ------------------------------------------------------


def test_intake_reduces_remaining_capacity(client, operator_headers, facility, vehicle):
    response = intake(client, operator_headers, facility["id"], vehicle.id, 300)
    assert response.status_code == 201
    assert response.json()["remainingCapacityKg"] == 700
    detail = client.get(f"/api/v1/facilities/{facility['id']}", headers=operator_headers).json()
    assert detail["remainingCapacityKg"] == 700
    assert detail["usedTodayKg"] == 300


def test_intake_over_capacity_rejected(client, operator_headers, facility, vehicle):
    intake(client, operator_headers, facility["id"], vehicle.id, 300)
    response = intake(client, operator_headers, facility["id"], vehicle.id, 800)
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "CAPACITY_EXCEEDED"
    detail = client.get(f"/api/v1/facilities/{facility['id']}", headers=operator_headers).json()
    assert detail["remainingCapacityKg"] == 700


@pytest.mark.parametrize("weight", [0, -50])
def test_intake_invalid_weight(client, operator_headers, facility, vehicle, weight):
    assert intake(client, operator_headers, facility["id"], vehicle.id, weight).status_code == 422


def test_intake_unknown_vehicle(client, operator_headers, facility):
    response = intake(client, operator_headers, facility["id"], 999, 10)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "UNKNOWN_VEHICLE"


def test_intake_wrong_waste_type(client, operator_headers, facility, vehicle):
    response = intake(client, operator_headers, facility["id"], vehicle.id, 10, waste="HAZARDOUS")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "WASTE_TYPE_NOT_ACCEPTED"


def test_intake_unloads_vehicle(client, operator_headers, facility, vehicle, db_session):
    intake(client, operator_headers, facility["id"], vehicle.id, 300)
    db_session.refresh(vehicle)
    assert vehicle.current_load_kg == 600


def test_only_operators_record_intake(client, admin_headers, citizen_headers, facility, vehicle):
    assert intake(client, admin_headers, facility["id"], vehicle.id, 10).status_code == 403
    assert intake(client, citizen_headers, facility["id"], vehicle.id, 10).status_code == 403


def test_back_to_back_deliveries_never_exceed_capacity(client, operator_headers, facility, vehicle):
    # TC-FAC-01 step 11: two deliveries whose total is above what is left.
    first = intake(client, operator_headers, facility["id"], vehicle.id, 600)
    second = intake(client, operator_headers, facility["id"], vehicle.id, 600)
    assert [first.status_code, second.status_code] == [201, 409]
    detail = client.get(f"/api/v1/facilities/{facility['id']}", headers=operator_headers).json()
    assert detail["usedTodayKg"] == 600


def test_yesterdays_deliveries_do_not_count(client, operator_headers, facility, vehicle, db_session):
    intake(client, operator_headers, facility["id"], vehicle.id, 900)
    record = db_session.query(FacilityIntake).one()
    record.recorded_at = datetime.now(timezone.utc) - timedelta(days=1)
    db_session.commit()
    detail = client.get(f"/api/v1/facilities/{facility['id']}", headers=operator_headers).json()
    assert detail["remainingCapacityKg"] == 1000


def test_intake_list(client, operator_headers, facility, vehicle):
    intake(client, operator_headers, facility["id"], vehicle.id, 100)
    intake(client, operator_headers, facility["id"], vehicle.id, 50, waste="GARDEN")
    rows = client.get(f"/api/v1/facilities/{facility['id']}/intakes", headers=operator_headers).json()
    assert [r["weightKg"] for r in rows] == [100, 50]


# --- exclusion from routing (TC-FAC-01 steps 9-10, SCW-F-032) -----------------


def test_full_wrong_type_and_small_facilities_excluded(client, admin_headers, operator_headers, vehicle, db_session):
    full = client.post("/api/v1/facilities", json=facility_payload(name="Full", dailyCapacityKg=100), headers=admin_headers).json()
    garden_only = client.post(
        "/api/v1/facilities", json=facility_payload(name="Garden", acceptedWasteTypes=["GARDEN"]), headers=admin_headers
    ).json()
    small = client.post("/api/v1/facilities", json=facility_payload(name="Small", dailyCapacityKg=200), headers=admin_headers).json()
    good = client.post("/api/v1/facilities", json=facility_payload(name="Good"), headers=admin_headers).json()
    intake(client, operator_headers, full["id"], vehicle.id, 100)

    names = [f.name for f in suitable_facilities(db_session, {"MIXED"}, 300)]
    assert names == ["Good"]
    assert garden_only["id"] not in [f.id for f in suitable_facilities(db_session, {"MIXED"}, 1)]
    assert small["id"] in [f.id for f in suitable_facilities(db_session, {"MIXED"}, 150)]

    for_routing = {f.id: f.remaining_capacity_kg for f in routing_facilities(db_session, today())}
    assert full["id"] not in for_routing
    assert for_routing[good["id"]] == 1000
