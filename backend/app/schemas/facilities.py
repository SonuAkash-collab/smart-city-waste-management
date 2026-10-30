"""Pydantic schemas for facilities (SCW-F-030 to SCW-F-032)."""

from pydantic import Field, field_validator, model_validator

from app.models.collection_request import WasteType
from app.schemas.base import CamelModel, UtcDateTime
from app.schemas.vehicles import clean_waste_types


class FacilityCreate(CamelModel):
    """Admin registers a disposal facility (SCW-F-030)."""

    name: str = Field(min_length=1, max_length=120)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accepted_waste_types: list[str] = Field(min_length=1)
    daily_capacity_kg: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("accepted_waste_types")
    @classmethod
    def check_waste_types(cls, values: list[str]) -> list[str]:
        return clean_waste_types(values)


class FacilityUpdate(CamelModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    accepted_waste_types: list[str] | None = Field(default=None, min_length=1)
    daily_capacity_kg: float | None = Field(default=None, gt=0)

    @model_validator(mode="before")
    @classmethod
    def reject_nulls(cls, data: object) -> object:
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None:
                    raise ValueError(f"{key} cannot be null")
        return data

    @field_validator("accepted_waste_types")
    @classmethod
    def check_waste_types(cls, values: list[str] | None) -> list[str] | None:
        return None if values is None else clean_waste_types(values)


class FacilityRead(CamelModel):
    id: int
    name: str
    latitude: float
    longitude: float
    accepted_waste_types: list[str]
    daily_capacity_kg: float
    used_today_kg: float = 0.0
    remaining_capacity_kg: float = 0.0
    remaining_percent: float = 0.0


class IntakeCreate(CamelModel):
    """Operator records an incoming delivery (SCW-F-031)."""

    vehicle_id: int = Field(gt=0)
    waste_type: WasteType
    weight_kg: float = Field(gt=0)


class IntakeRead(CamelModel):
    id: int
    facility_id: int
    vehicle_id: int
    operator_id: int
    waste_type: WasteType
    weight_kg: float
    recorded_at: UtcDateTime
    remaining_capacity_kg: float
