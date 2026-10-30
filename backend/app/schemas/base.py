"""Shared schema base classes.

The API speaks camelCase JSON (for example ``wasteType`` and
``estimatedQuantityKg`` in SAD section 4.3) while the Python code keeps
snake_case. ``CamelModel`` converts between the two and still accepts
snake_case input.
"""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainSerializer
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model that reads and writes camelCase JSON."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


def to_utc_iso(value: datetime) -> str:
    """Write datetimes as UTC ISO strings ending in Z.

    SQLite returns naive datetimes; they are stored in UTC, so treat them as UTC.
    """
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


UtcDateTime = Annotated[datetime, PlainSerializer(to_utc_iso, return_type=str)]
