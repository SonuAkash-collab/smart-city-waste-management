"""Geographic calculation helpers."""

import math


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Return the great-circle distance between two coordinates in km."""
    earth_radius_km = 6371.0
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    # Protect against tiny floating-point rounding errors.
    a = min(1.0, max(0.0, a))

    central_angle = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return earth_radius_km * central_angle
