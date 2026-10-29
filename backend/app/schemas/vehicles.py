
"""Pydantic schemas for vehicle management and driver assignment."""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.models.vehicle import VehicleStatus


class VehicleCreate(BaseModel):
    """Validate data required to create a vehicle."""

    registration_number: str = Field(min_length=1, max_length=20)
    capacity_kg: float = Field(gt=0)
    waste_types: list[str] = Field(min_length=1)
    depot_latitude: float = Field(ge=-90, le=90)
    depot_longitude: float = Field(ge=-180, le=180)

    @field_validator("registration_number")
    @classmethod
    def normalize_registration_number(cls, value: str) -> str:
        """Normalize vehicle registration numbers."""
        value = value.strip().upper()
        if not value:
            raise ValueError("Registration number cannot be empty")
        return value

    @field_validator("waste_types")
    @classmethod
    def validate_waste_types(cls, values: list[str]) -> list[str]:
        """Reject empty waste type values."""
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("Waste types cannot be empty")
        return normalized


class VehicleUpdate(BaseModel):
    """Validate fields that can be updated on an existing vehicle."""

    registration_number: str | None = Field(
        default=None, min_length=1, max_length=20
    )
    capacity_kg: float | None = Field(default=None, gt=0)
    waste_types: list[str] | None = Field(default=None, min_length=1)
    depot_latitude: float | None = Field(default=None, ge=-90, le=90)
    depot_longitude: float | None = Field(default=None, ge=-180, le=180)
    status: VehicleStatus | None = None

    @model_validator(mode="before")
    @classmethod
    def reject_explicit_nulls(cls, data: object) -> object:
        """Reject null for supplied fields while allowing omitted fields."""
        if isinstance(data, dict):
            non_nullable_fields = {
                "registration_number",
                "capacity_kg",
                "waste_types",
                "depot_latitude",
                "depot_longitude",
                "status",
            }
            for field in non_nullable_fields:
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")
        return data

    @field_validator("registration_number")
    @classmethod
    def normalize_registration_number(
        cls, value: str | None
    ) -> str | None:
        """Normalize registration numbers when provided."""
        if value is None:
            return None
        value = value.strip().upper()
        if not value:
            raise ValueError("Registration number cannot be empty")
        return value

    @field_validator("waste_types")
    @classmethod
    def validate_waste_types(
        cls, values: list[str] | None
    ) -> list[str] | None:
        """Reject empty waste type values."""
        if values is None:
            return None
        normalized = [value.strip() for value in values]
        if any(not value for value in normalized):
            raise ValueError("Waste types cannot be empty")
        return normalized


class VehicleRead(BaseModel):
    """Represent a vehicle in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_number: str
    capacity_kg: float
    current_load_kg: float
    waste_types: list[str]
    depot_latitude: float
    depot_longitude: float
    status: VehicleStatus
    driver_id: int | None


class DriverAssignmentRequest(BaseModel):
    """Validate a driver assignment request."""

    driver_id: int = Field(gt=0)
