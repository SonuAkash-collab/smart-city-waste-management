
"""API endpoints for vehicle management and driver assignment."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.vehicles import (
    DriverAssignmentRequest,
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)
from app.services.vehicles import (
    DriverAlreadyAssignedError,
    DriverNotFoundError,
    InvalidDriverError,
    VehicleConflictError,
    VehicleNotFoundError,
    assign_driver,
    create_vehicle,
    get_vehicle,
    list_vehicles,
    update_vehicle,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[VehicleRead])
def get_vehicles(db: Session = Depends(get_db)):
    """List all vehicles."""
    return list_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleRead)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    """Retrieve a vehicle by ID."""
    try:
        return get_vehicle(db, vehicle_id)
    except VehicleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/",
    response_model=VehicleRead,
    status_code=status.HTTP_201_CREATED,
)
def add_vehicle(data: VehicleCreate, db: Session = Depends(get_db)):
    """Create a vehicle."""
    try:
        return create_vehicle(db, data)
    except VehicleConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{vehicle_id}", response_model=VehicleRead)
def edit_vehicle(
    vehicle_id: int,
    data: VehicleUpdate,
    db: Session = Depends(get_db),
):
    """Update vehicle details or status."""
    try:
        return update_vehicle(db, vehicle_id, data)
    except VehicleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except VehicleConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.patch("/{vehicle_id}/driver", response_model=VehicleRead)
def assign_vehicle_driver(
    vehicle_id: int,
    data: DriverAssignmentRequest,
    db: Session = Depends(get_db),
):
    """Assign an active driver to a vehicle."""
    try:
        return assign_driver(db, vehicle_id, data.driver_id)
    except VehicleNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except DriverNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidDriverError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    except DriverAlreadyAssignedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
