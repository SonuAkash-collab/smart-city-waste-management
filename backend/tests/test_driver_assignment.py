"""Tests for assigning drivers to vehicles."""

from app.models.user import User, UserRole
from app.models.vehicle import Vehicle, VehicleStatus


def create_vehicle(db_session):
    """Create a vehicle for testing."""
    vehicle = Vehicle(
        registration_number="KA01AB1234",
        capacity_kg=1000,
        current_load_kg=0,
        waste_types=["MIXED"],
        depot_latitude=12.9716,
        depot_longitude=77.5946,
        status=VehicleStatus.AVAILABLE,
    )
    db_session.add(vehicle)
    db_session.commit()
    db_session.refresh(vehicle)
    return vehicle


def create_user(db_session, role=UserRole.DRIVER, is_active=True):
    """Create a user for testing."""
    user = User(
        email="driver@example.com",
        hashed_password="test-hash",
        full_name="Test Driver",
        role=role,
        is_active=is_active,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_assign_active_driver_successfully(client, db_session):
    """Assign an active driver to an existing vehicle."""
    vehicle = create_vehicle(db_session)
    driver = create_user(db_session)

    response = client.patch(
        f"/api/v1/vehicles/{vehicle.id}/driver",
        json={"driver_id": driver.id},
    )

    assert response.status_code == 200
    assert response.json()["id"] == vehicle.id
    assert response.json()["driverId"] == driver.id


def test_assign_driver_to_missing_vehicle_returns_404(client, db_session):
    """Return 404 when the vehicle does not exist."""
    driver = create_user(db_session)

    response = client.patch(
        "/api/v1/vehicles/999/driver",
        json={"driver_id": driver.id},
    )

    assert response.status_code == 404


def test_assign_missing_driver_returns_404(client, db_session):
    """Return 404 when the driver does not exist."""
    vehicle = create_vehicle(db_session)

    response = client.patch(
        f"/api/v1/vehicles/{vehicle.id}/driver",
        json={"driver_id": 999},
    )

    assert response.status_code == 404


def test_assign_non_driver_user_returns_422(client, db_session):
    """Reject a user without the DRIVER role."""
    vehicle = create_vehicle(db_session)
    user = create_user(db_session, role=UserRole.CITIZEN)

    response = client.patch(
        f"/api/v1/vehicles/{vehicle.id}/driver",
        json={"driver_id": user.id},
    )

    assert response.status_code == 422


def test_assign_inactive_driver_returns_422(client, db_session):
    """Reject an inactive driver."""
    vehicle = create_vehicle(db_session)
    driver = create_user(db_session, is_active=False)

    response = client.patch(
        f"/api/v1/vehicles/{vehicle.id}/driver",
        json={"driver_id": driver.id},
    )

    assert response.status_code == 422


def test_assign_driver_rejects_invalid_driver_id(client):
    """Reject a non-positive driver ID."""
    response = client.patch(
        "/api/v1/vehicles/1/driver",
        json={"driver_id": 0},
    )

    assert response.status_code == 422


def test_driver_cannot_drive_two_vehicles(client, db_session, make_user):
    """Reject assigning a driver who already drives another vehicle (TC-VEH-02 step 5)."""
    first = create_vehicle(db_session)
    second = Vehicle(
        registration_number="KA02CD5678",
        capacity_kg=800,
        current_load_kg=0,
        waste_types=["MIXED"],
        depot_latitude=12.9716,
        depot_longitude=77.5946,
        status=VehicleStatus.AVAILABLE,
    )
    db_session.add(second)
    db_session.commit()
    driver = make_user(UserRole.DRIVER)

    assert client.patch(f"/api/v1/vehicles/{first.id}/driver", json={"driver_id": driver.id}).status_code == 200
    again = client.patch(f"/api/v1/vehicles/{first.id}/driver", json={"driver_id": driver.id})
    assert again.status_code == 200  # same vehicle again is fine

    response = client.patch(f"/api/v1/vehicles/{second.id}/driver", json={"driver_id": driver.id})
    assert response.status_code == 409
    db_session.refresh(second)
    assert second.driver_id is None
