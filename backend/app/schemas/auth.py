"""Pydantic schemas for auth."""

import re

from pydantic import Field, field_validator

from app.models.user import UserRole
from app.schemas.base import CamelModel

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_email(value: str) -> str:
    value = value.strip().lower()
    if not EMAIL_PATTERN.match(value):
        raise ValueError("Enter a valid email address")
    return value


class RegisterRequest(CamelModel):
    """Self-registration always creates a Citizen account (SCW-F-001)."""

    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=1, max_length=120)

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


class LoginRequest(CamelModel):
    email: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=72)

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        return value.strip().lower()


class UserOut(CamelModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool


class TokenResponse(CamelModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserOut
