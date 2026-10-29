import enum

from sqlalchemy import JSON, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class VehicleStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ON_ROUTE = "ON_ROUTE"
    MAINTENANCE = "MAINTENANCE"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    registration_number: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    capacity_kg: Mapped[float] = mapped_column(Float)
    current_load_kg: Mapped[float] = mapped_column(Float, default=0.0)
    waste_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    depot_latitude: Mapped[float] = mapped_column(Float)
    depot_longitude: Mapped[float] = mapped_column(Float)
    status: Mapped[VehicleStatus] = mapped_column(
        Enum(VehicleStatus, native_enum=False, length=20), default=VehicleStatus.AVAILABLE
    )
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
