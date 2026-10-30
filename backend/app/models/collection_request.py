import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class WasteType(str, enum.Enum):
    HAZARDOUS = "HAZARDOUS"
    MEDICAL = "MEDICAL"
    E_WASTE = "E_WASTE"
    MIXED = "MIXED"
    RECYCLABLE = "RECYCLABLE"
    GARDEN = "GARDEN"
    BULKY = "BULKY"


class RequestStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    COLLECTED = "COLLECTED"
    REJECTED = "REJECTED"
    MISSED = "MISSED"
    CANCELLED = "CANCELLED"


class Priority(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class CollectionRequest(Base):
    __tablename__ = "collection_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    citizen_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    waste_type: Mapped[WasteType] = mapped_column(Enum(WasteType, native_enum=False, length=20))
    estimated_quantity_kg: Mapped[float] = mapped_column(Float)
    photo: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RequestStatus] = mapped_column(
        Enum(RequestStatus, native_enum=False, length=20), default=RequestStatus.SUBMITTED, index=True
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, native_enum=False, length=20), default=Priority.MEDIUM
    )
    priority_overridden: Mapped[bool] = mapped_column(Boolean, default=False)
    priority_escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @property
    def has_photo(self) -> bool:
        return bool(self.photo)
