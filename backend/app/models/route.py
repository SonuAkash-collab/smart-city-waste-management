import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class RouteStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class StopType(str, enum.Enum):
    COLLECTION = "COLLECTION"
    FACILITY = "FACILITY"


class StopStatus(str, enum.Enum):
    PENDING = "PENDING"
    COLLECTED = "COLLECTED"
    MISSED = "MISSED"


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_date: Mapped[date] = mapped_column(Date, index=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    status: Mapped[RouteStatus] = mapped_column(
        Enum(RouteStatus, native_enum=False, length=20), default=RouteStatus.PLANNED
    )
    total_distance_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    stops: Mapped[list["RouteStop"]] = relationship(
        back_populates="route", order_by="RouteStop.sequence", cascade="all, delete-orphan"
    )


class RouteStop(Base):
    __tablename__ = "route_stops"

    id: Mapped[int] = mapped_column(primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id"), index=True)
    sequence: Mapped[int] = mapped_column(Integer)
    stop_type: Mapped[StopType] = mapped_column(
        Enum(StopType, native_enum=False, length=20), default=StopType.COLLECTION
    )
    request_id: Mapped[int | None] = mapped_column(ForeignKey("collection_requests.id"), nullable=True)
    facility_id: Mapped[int | None] = mapped_column(ForeignKey("facilities.id"), nullable=True)
    status: Mapped[StopStatus] = mapped_column(
        Enum(StopStatus, native_enum=False, length=20), default=StopStatus.PENDING
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    route: Mapped[Route] = relationship(back_populates="stops")
