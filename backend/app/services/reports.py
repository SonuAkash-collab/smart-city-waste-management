"""Daily collection report as CSV (SCW-F-052)."""

import csv
import io
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.collection_request import CollectionRequest
from app.models.route import Route, RouteStop
from app.models.user import User
from app.models.vehicle import Vehicle

COLUMNS = [
    "date", "route_id", "vehicle_registration", "driver_name", "request_id",
    "waste_type", "quantity_kg", "stop_status", "facility_id",
]


def daily_rows(db: Session, day: date) -> list[list]:
    """One row per route stop of the routes planned for ``day``."""
    rows = []
    routes = db.scalars(select(Route).where(Route.route_date == day).order_by(Route.id)).all()
    for route in routes:
        vehicle = db.get(Vehicle, route.vehicle_id)
        driver = db.get(User, vehicle.driver_id) if vehicle.driver_id else None
        for stop in db.scalars(select(RouteStop).where(RouteStop.route_id == route.id).order_by(RouteStop.sequence)):
            request = db.get(CollectionRequest, stop.request_id) if stop.request_id else None
            rows.append([
                day.isoformat(),
                route.id,
                vehicle.registration_number,
                driver.full_name if driver else "",
                request.id if request else "",
                request.waste_type.value if request else "",
                request.estimated_quantity_kg if request else "",
                stop.status.value,
                stop.facility_id or "",
            ])
    return rows


def daily_csv(db: Session, day: date) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(COLUMNS)
    writer.writerows(daily_rows(db, day))
    return buffer.getvalue()
