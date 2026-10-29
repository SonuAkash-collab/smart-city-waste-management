import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class UserRole(str, enum.Enum):
    CITIZEN = "CITIZEN"
    DRIVER = "DRIVER"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, native_enum=False, length=20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
