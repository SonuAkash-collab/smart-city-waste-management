"""Shared schema base classes.

The API speaks camelCase JSON (for example ``wasteType`` and
``estimatedQuantityKg`` in SAD section 4.3) while the Python code keeps
snake_case. ``CamelModel`` converts between the two and still accepts
snake_case input.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model that reads and writes camelCase JSON."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
