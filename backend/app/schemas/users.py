"""Pydantic schemas for users."""

from typing import Literal

from pydantic import Field, field_validator

from app.schemas.auth import normalize_email
from app.schemas.base import CamelModel


class StaffCreate(CamelModel):
    """Admin creates a Driver or Operator with a temporary password (SCW-F-003)."""

    email: str = Field(max_length=255)
    full_name: str = Field(min_length=1, max_length=120)
    role: Literal["DRIVER", "OPERATOR"]
    temporary_password: str = Field(min_length=8, max_length=72)

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        return normalize_email(value)

    @field_validator("full_name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class UserStatusUpdate(CamelModel):
    is_active: bool
