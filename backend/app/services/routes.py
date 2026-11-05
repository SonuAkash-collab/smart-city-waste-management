"""Business logic for routes: generate, store and run them (SCW-F-040 to SCW-F-044)."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.collection_request import CollectionRequest, RequestStatus
from app.models.facility import Facility
from app.models.route import Route, RouteStatus, RouteStop, StopStatus, StopType
from app.models.user import User, UserRole
from app.models.vehicle import Vehicle, VehicleStatus
from app.services import route_engine
from app.services.facilities import routing_facilities
from app.services.notifications import notify
from app.services.requests import announce_status, escalate_waiting_requests, utcnow
from app.services.vehicles import VehicleOverloadError, add_load, unload

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


def alert_admins(db: Session, message: str) -> None:
    """Send an in-app alert to every active Admin (TC-RT-04 step 5)."""
    admins = db.scalars(
        select(User).where(User.role == UserRole.ADMIN, User.is_active.is_(True))
    ).all()
    for admin in admins:
        notify(db, admin.id, message)


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
    for alert in plan.alerts:
        alert_admins(db, f"Route alert for {day}: {alert.message}")
    if plan.unassigned:
        ids = ", ".join(f"#{u.request_id}" for u in plan.unassigned)
        alert_admins(
            db,
            f"Routes for {day}: {len(plan.unassigned)} approved request(s) could not be planned "
            f"({ids}). They stay Approved for the next run.",
        )

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


def _driver_vehicle_ids(db: Session, driver: User) -> list[int]:
    return list(db.scalars(select(Vehicle.id).where(Vehicle.driver_id == driver.id)).all())


def list_routes(db: Session, user: User, day: date | None = None) -> list[Route]:
    """Admins see every route; drivers only routes of the vehicle they drive."""
    query = select(Route).order_by(Route.route_date.desc(), Route.id)
    if user.role != UserRole.ADMIN:
        query = query.where(Route.vehicle_id.in_(_driver_vehicle_ids(db, user)))
    if day is not None:
        query = query.where(Route.route_date == day)
    return list(db.scalars(query.limit(100)).all())


def assigned_routes(db: Session, driver: User) -> list[Route]:
    """The driver's routes that are planned or under way (SCW-F-043)."""
    return list(
        db.scalars(
            select(Route)
            .where(
                Route.vehicle_id.in_(_driver_vehicle_ids(db, driver)),
                Route.status.in_(ACTIVE_ROUTE),
            )
            .order_by(Route.route_date, Route.id)
        ).all()
    )


def get_route(db: Session, route_id: int) -> Route:
    route = db.get(Route, route_id)
    if route is None:
        raise ApiError(404, "ROUTE_NOT_FOUND", "Route not found.")
    return route


def get_route_for(db: Session, user: User, route_id: int) -> Route:
    """A route for an Admin or the driver of its vehicle; other drivers get 403."""
    route = get_route(db, route_id)
    if user.role != UserRole.ADMIN and route.vehicle_id not in _driver_vehicle_ids(db, user):
        raise ApiError(403, "FORBIDDEN", "This route belongs to another driver.")
    return route


def update_stop(db: Session, driver: User, route_id: int, stop_id: int, outcome: str) -> dict:
    """Driver marks a stop Collected or Missed (SCW-F-044).

    * A collection stop updates its request to COLLECTED or MISSED, tells the
      citizen, and a collected load is added to the vehicle (SCW-F-023).
    * A facility stop marked Collected means the vehicle unloaded there.
    * The route becomes In progress at the first update and Completed when no
      stop is left; the vehicle is then Available again unless it is in
      Maintenance (SCW-F-021).
    """
    route = get_route_for(db, driver, route_id)
    stop = next((s for s in route.stops if s.id == stop_id), None)
    if stop is None:
        raise ApiError(404, "STOP_NOT_FOUND", "This stop is not on the route.")
    if route.status == RouteStatus.COMPLETED:
        raise ApiError(409, "ROUTE_COMPLETED", "This route is already completed.")
    if stop.status != StopStatus.PENDING:
        raise ApiError(409, "STOP_ALREADY_DONE", f"This stop is already {stop.status.value}.")

    new_status = StopStatus(outcome)
    vehicle = db.get(Vehicle, route.vehicle_id)
    request = db.get(CollectionRequest, stop.request_id) if stop.request_id else None

    if stop.stop_type == StopType.COLLECTION and new_status == StopStatus.COLLECTED:
        try:
            add_load(db, vehicle.id, request.estimated_quantity_kg)
        except VehicleOverloadError as exc:
            raise ApiError(409, "VEHICLE_FULL", str(exc)) from exc
    if stop.stop_type == StopType.FACILITY and new_status == StopStatus.COLLECTED:
        unload(db, vehicle.id)

    stop.status = new_status
    stop.completed_at = utcnow()
    if request is not None:
        request.status = (
            RequestStatus.COLLECTED if new_status == StopStatus.COLLECTED else RequestStatus.MISSED
        )
        request.updated_at = utcnow()

    route.status = RouteStatus.IN_PROGRESS
    if all(s.status != StopStatus.PENDING for s in route.stops):
        route.status = RouteStatus.COMPLETED
        if vehicle.status != VehicleStatus.MAINTENANCE:
            vehicle.status = VehicleStatus.AVAILABLE
    db.commit()
    db.refresh(vehicle)

    if request is not None:
        announce_status(db, request)
    return {
        "route_id": route.id,
        "stop_id": stop.id,
        "request_id": stop.request_id,
        "status": stop.status,
        "request_status": request.status.value if request else None,
        "route_status": route.status,
        "vehicle_load_kg": vehicle.current_load_kg,
    }
