"""Business logic for collection requests (SCW-F-010 to SCW-F-014)."""

from app.models.collection_request import Priority, WasteType

# SCW-F-011: priority from waste type.
PRIORITY_BY_WASTE_TYPE = {
    WasteType.HAZARDOUS: Priority.HIGH,
    WasteType.MEDICAL: Priority.HIGH,
    WasteType.E_WASTE: Priority.HIGH,
    WasteType.MIXED: Priority.MEDIUM,
    WasteType.RECYCLABLE: Priority.MEDIUM,
    WasteType.GARDEN: Priority.LOW,
    WasteType.BULKY: Priority.LOW,
}


def initial_priority(waste_type: WasteType) -> Priority:
    """Return the starting priority for a waste type."""
    return PRIORITY_BY_WASTE_TYPE[waste_type]
