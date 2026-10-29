
"""Tests for vehicle management endpoints."""

from app.models.vehicle import Vehicle


def vehicle_payload():
    """Return valid data for creating a vehicle."""
    return {
        "registration_number": "KA01AB1234",
        "capacity_kg": 1000,
        "waste_types": ["GENERAL", "RECYCLABLE"],
        "depot_latitude": 12.9716,
        "depot_longitude": 77.5946,
    }


def test_create_vehicle(client):
    """Create a vehicle successfully."""
    response = client.post("/api/v1/vehicles/", json=vehicle_payload())

    assert response.status_code == 201
    data = response.json()
    assert data["registration_number"] == "KA01AB1234"
    assert data["capacity_kg"] == 1000
    assert data["current_load_kg"] == 0
    assert data["status"] == "AVAILABLE"


def test_list_vehicles(client):
    """List vehicles successfully."""
    client.post("/api/v1/vehicles/", json=vehicle_payload())

    response = client.get("/api/v1/vehicles/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["registration_number"] == "KA01AB1234"


def test_update_vehicle_status(client):
    """Update a vehicle's status."""
    created = client.post("/api/v1/vehicles/", json=vehicle_payload())
    vehicle_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/vehicles/{vehicle_id}",
        json={"status": "MAINTENANCE"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "MAINTENANCE"


def test_duplicate_registration_rejected(client):
    """Reject duplicate registration numbers."""
    client.post("/api/v1/vehicles/", json=vehicle_payload())

    duplicate = vehicle_payload()
    duplicate["registration_number"] = " ka01ab1234 "

    response = client.post("/api/v1/vehicles/", json=duplicate)

    assert response.status_code == 409


def test_invalid_vehicle_capacity_rejected(client):
    """Reject zero capacity when creating a vehicle."""
    payload = vehicle_payload()
    payload["capacity_kg"] = 0

    response = client.post("/api/v1/vehicles/", json=payload)

    assert response.status_code == 422


def test_missing_vehicle_returns_404(client):
    """Return 404 for a missing vehicle."""
    response = client.get("/api/v1/vehicles/999")

    assert response.status_code == 404


def test_update_vehicle_rejects_null_capacity(client):
    """Reject explicit null for a non-nullable capacity field."""
    created = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload(),
    )
    assert created.status_code == 201

    vehicle_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/vehicles/{vehicle_id}",
        json={"capacity_kg": None},
    )

    assert response.status_code == 422


def test_update_rejects_capacity_below_current_load(client, db_session):
    """Reject capacity below the vehicle's current load."""
    created = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload(),
    )
    assert created.status_code == 201

    vehicle_id = created.json()["id"]
    vehicle = db_session.get(Vehicle, vehicle_id)
    assert vehicle is not None

    vehicle.current_load_kg = 700
    db_session.commit()

    response = client.patch(
        f"/api/v1/vehicles/{vehicle_id}",
        json={"capacity_kg": 500},
    )

    assert response.status_code == 409


def test_update_rejects_invalid_capacity(client):
    """Reject non-positive capacity during update."""
    created = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload(),
    )
    vehicle_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/vehicles/{vehicle_id}",
        json={"capacity_kg": 0},
    )

    assert response.status_code == 422


def test_update_omitted_fields_remain_unchanged(client):
    """Preserve omitted fields during a partial update."""
    created = client.post(
        "/api/v1/vehicles/",
        json=vehicle_payload(),
    )
    vehicle_id = created.json()["id"]

    response = client.patch(
        f"/api/v1/vehicles/{vehicle_id}",
        json={"status": "MAINTENANCE"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["capacity_kg"] == 1000
    assert data["registration_number"] == "KA01AB1234"
    assert data["status"] == "MAINTENANCE"
