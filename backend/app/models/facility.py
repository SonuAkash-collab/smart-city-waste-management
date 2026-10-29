from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    accepted_waste_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    daily_capacity_kg: Mapped[float] = mapped_column(Float)


class FacilityIntake(Base):
    __tablename__ = "facility_intakes"

    id: Mapped[int] = mapped_column(primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"), index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    weight_kg: Mapped[float] = mapped_column(Float)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
