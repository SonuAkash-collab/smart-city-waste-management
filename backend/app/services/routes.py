"""Business logic for routes: generate, store and run them (SCW-F-040 to SCW-F-044)."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.collection_request import CollectionRequest, RequestStatus
from app.models.facility import Facility
from app.models.route import Route, RouteStatus, RouteStop, StopStatus, StopType
from app.models.user import User
from app.models.vehicle import Vehicle, VehicleStatus
from app.services import route_engine
from app.services.facilities import routing_facilities
from app.services.requests import announce_status, escalate_waiting_requests, utcnow

ACTIVE_ROUTE = (RouteStatus.PLANNED, RouteStatus.IN_PROGRESS)


def describe_route(db: Session, route: Route) -> dict:
    """A route with its vehicle, driver and stops, for API responses."""
    vehicle = db.get(Vehicle, route.vehicle_id)
    driver = db.get(User, vehicle.driver_id) if vehicle.driver_id else None
    stops = []
    for stop in route.stops:
        item = {
            "id": stop.id,
            "sequence": stop.sequence,
            "stop_type": stop.stop_type,
            "status": stop.status,
            "latitude": stop.latitude,
            "longitude": stop.longitude,
            "load_after_kg": stop.load_after_kg,
            "distance_km": stop.distance_km,
            "completed_at": stop.completed_at,
            "request_id": stop.request_id,
            "facility_id": stop.facility_id,
        }
        if stop.request_id:
            request = db.get(CollectionRequest, stop.request_id)
            item.update(
                address=request.address,
                waste_type=request.waste_type,
                quantity_kg=request.estimated_quantity_kg,
            )
        if stop.facility_id:
            item["facility_name"] = db.get(Facility, stop.facility_id).name
        stops.append(item)
    return {
        "id": route.id,
        "date": route.route_date,
        "status": route.status,
        "vehicle_id": vehicle.id,
        "vehicle_registration": vehicle.registration_number,
        "vehicle_capacity_kg": vehicle.capacity_kg,
        "vehicle_status": vehicle.status,
        "driver_id": driver.id if driver else None,
        "driver_name": driver.full_name if driver else None,
        "total_distance_km": route.total_distance_km,
        "stops": stops,
    }


def _engine_inputs(db: Session, day: date):
    requests = db.scalars(
        select(CollectionRequest)
        .where(CollectionRequest.status == RequestStatus.APPROVED)
        .order_by(CollectionRequest.id)
    ).all()
    # Only Available vehicles with a driver can run a route (SCW-F-021, SCW-F-022).
    vehicles = db.scalars(
        select(Vehicle)
        .where(Vehicle.status == VehicleStatus.AVAILABLE, Vehicle.driver_id.is_not(None))
        .order_by(Vehicle.id)
    ).all()
    request_inputs = [
        route_engine.RequestInput(
            id=r.id,
            latitude=r.latitude,
            longitude=r.longitude,
            waste_type=r.waste_type.value,
            quantity_kg=r.estimated_quantity_kg,
            priority=r.priority.value,
        )
        for r in requests
    ]
    vehicle_inputs = [
        route_engine.VehicleInput(
            id=v.id,
            capacity_kg=v.capacity_kg,
            waste_types=tuple(v.waste_types),
            depot_latitude=v.depot_latitude,
            depot_longitude=v.depot_longitude,
            current_load_kg=v.current_load_kg,
        )
        for v in vehicles
    ]
    return request_inputs, vehicle_inputs, routing_facilities(db, day)


def generate_routes(db: Session, day: date) -> dict:
    """Plan and save routes for ``day`` from every Approved request (SCW-F-040)."""
    existing = db.scalar(
        select(Route).where(Route.route_date == day, Route.status.in_(ACTIVE_ROUTE))
    )
    if existing is not None:
        raise ApiError(
            409,
            "ROUTES_EXIST",
            "Routes for this date are already planned. Finish them before planning again.",
        )

    escalate_waiting_requests(db)
    requests, vehicles, facilities = _engine_inputs(db, day)
    plan = route_engine.plan_routes(requests, vehicles, facilities)

    saved: list[Route] = []
    scheduled: list[CollectionRequest] = []
    for planned in plan.routes:
        route = Route(
            route_date=day,
            vehicle_id=planned.vehicle_id,
            status=RouteStatus.PLANNED,
            total_distance_km=planned.total_distance_km,
        )
        for stop in planned.stops:
            route.stops.append(
                RouteStop(
                    sequence=stop.sequence,
                    stop_type=StopType(stop.stop_type),
                    request_id=stop.request_id,
                    facility_id=stop.facility_id,
                    latitude=stop.latitude,
                    longitude=stop.longitude,
                    load_after_kg=stop.load_after_kg,
                    distance_km=stop.distance_km,
                    status=StopStatus.PENDING,
                )
            )
            if stop.request_id:
                request = db.get(CollectionRequest, stop.request_id)
                request.status = RequestStatus.SCHEDULED
                request.updated_at = utcnow()
                scheduled.append(request)
        # A vehicle with an active route is On Route (SCW-F-021).
        db.get(Vehicle, planned.vehicle_id).status = VehicleStatus.ON_ROUTE
        db.add(route)
        saved.append(route)
    db.commit()

    for request in scheduled:
        announce_status(db, request)

    count = len(saved)
    return {
        "date": day,
        "routes": [describe_route(db, route) for route in saved],
        "unassigned": [{"request_id": u.request_id, "reason": u.reason} for u in plan.unassigned],
        "alerts": [
            {
                "vehicle_id": a.vehicle_id,
                "load_kg": a.load_kg,
                "waste_types": list(a.waste_types),
                "message": a.message,
            }
            for a in plan.alerts
        ],
        "message": (
            f"{count} route{'s' if count != 1 else ''} planned with {len(scheduled)} stops."
            if count
            else "No routes planned: no approved requests or no available vehicles with a driver."
        ),
    }
