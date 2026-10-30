
"""Business logic for vehicle management and driver assignment."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.vehicles import VehicleCreate, VehicleUpdate


class VehicleNotFoundError(Exception):
    """Raised when a requested vehicle does not exist."""


class VehicleConflictError(Exception):
    """Raised when a vehicle operation conflicts with existing data."""


class VehicleOverloadError(Exception):
    """Raised when a load would go above the vehicle's capacity."""


class DriverAlreadyAssignedError(Exception):
    """Raised when a driver already drives another vehicle."""


class DriverNotFoundError(Exception):
    """Raised when the requested driver does not exist."""


class InvalidDriverError(Exception):
    """Raised when a user is not eligible to be a driver."""


def list_vehicles(db: Session) -> list[Vehicle]:
    """Return all vehicles ordered by ID."""
    return list(db.scalars(select(Vehicle).order_by(Vehicle.id)).all())


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle:
    """Return one vehicle or raise an error if it does not exist."""
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise VehicleNotFoundError("Vehicle not found")
    return vehicle


def create_vehicle(db: Session, data: VehicleCreate) -> Vehicle:
    """Create a vehicle after checking registration uniqueness."""
    registration = data.registration_number

    existing = db.scalar(
        select(Vehicle).where(Vehicle.registration_number == registration)
    )
    if existing is not None:
        raise VehicleConflictError("Registration number already exists")

    vehicle = Vehicle(
        registration_number=registration,
        capacity_kg=data.capacity_kg,
        current_load_kg=0.0,
        waste_types=data.waste_types,
        depot_latitude=data.depot_latitude,
        depot_longitude=data.depot_longitude,
        status=VehicleStatus.AVAILABLE,
    )
    db.add(vehicle)

    try:
        db.commit()
        db.refresh(vehicle)
    except IntegrityError as exc:
        db.rollback()
        raise VehicleConflictError(
            "Registration number already exists"
        ) from exc

    return vehicle


def update_vehicle(
    db: Session, vehicle_id: int, data: VehicleUpdate
) -> Vehicle:
    """Update editable vehicle details and status."""
    vehicle = get_vehicle(db, vehicle_id)
    changes = data.model_dump(exclude_unset=True)

    new_registration = changes.get("registration_number")
    if new_registration is not None:
        existing = db.scalar(
            select(Vehicle).where(
                Vehicle.registration_number == new_registration,
                Vehicle.id != vehicle_id,
            )
        )
        if existing is not None:
            raise VehicleConflictError("Registration number already exists")

    new_capacity = changes.get("capacity_kg")
    if new_capacity is not None and new_capacity < vehicle.current_load_kg:
        raise VehicleConflictError(
            "Capacity cannot be lower than the vehicle's current load"
        )

    for field, value in changes.items():
        setattr(vehicle, field, value)

    try:
        db.commit()
        db.refresh(vehicle)
    except IntegrityError as exc:
        db.rollback()
        raise VehicleConflictError(
            "Vehicle update conflicts with existing data"
        ) from exc

    return vehicle


def assign_driver(
    db: Session,
    vehicle_id: int,
    driver_id: int,
) -> Vehicle:
    """Assign an active driver to an existing vehicle."""
    vehicle = db.get(Vehicle, vehicle_id)
    if vehicle is None:
        raise VehicleNotFoundError("Vehicle not found")

    driver = db.get(User, driver_id)
    if driver is None:
        raise DriverNotFoundError("Driver not found")

    if driver.role != UserRole.DRIVER:
        raise InvalidDriverError("User does not have the DRIVER role")

    if not driver.is_active:
        raise InvalidDriverError("Driver is inactive")

    # One driver drives at most one vehicle at a time.
    other = db.scalar(
        select(Vehicle).where(Vehicle.driver_id == driver.id, Vehicle.id != vehicle.id)
    )
    if other is not None:
        raise DriverAlreadyAssignedError(
            f"Driver is already assigned to vehicle {other.registration_number}"
        )

    vehicle.driver_id = driver.id
    db.commit()
    db.refresh(vehicle)

    return vehicle


def add_load(db: Session, vehicle_id: int, weight_kg: float) -> Vehicle:
    """Record collected waste on a vehicle (SCW-F-023).

    The load can never go above the vehicle's capacity.
    """
    vehicle = get_vehicle(db, vehicle_id)
    if weight_kg < 0:
        raise ValueError("Weight cannot be negative")
    new_load = vehicle.current_load_kg + weight_kg
    if new_load > vehicle.capacity_kg + 1e-9:
        raise VehicleOverloadError(
            f"Vehicle {vehicle.registration_number} would carry {new_load:.0f} kg "
            f"but its capacity is {vehicle.capacity_kg:.0f} kg"
        )
    vehicle.current_load_kg = round(new_load, 3)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def unload(db: Session, vehicle_id: int, weight_kg: float | None = None) -> Vehicle:
    """Remove waste from a vehicle at a facility; no weight means unload everything."""
    vehicle = get_vehicle(db, vehicle_id)
    if weight_kg is None:
        vehicle.current_load_kg = 0.0
    else:
        vehicle.current_load_kg = round(max(0.0, vehicle.current_load_kg - weight_kg), 3)
    db.commit()
    db.refresh(vehicle)
    return vehicle
