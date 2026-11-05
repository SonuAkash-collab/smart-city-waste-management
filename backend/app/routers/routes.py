from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import User, UserRole
from app.schemas.routes import GenerateResult, GenerateRoutes, RouteOut, StopUpdate, StopUpdated
from app.services import routes as route_service

router = APIRouter(prefix="/routes", tags=["routes"])


@router.post(
    "/generate",
    response_model=GenerateResult,
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)
def generate(data: GenerateRoutes, db: Session = Depends(get_db)):
    """Admin plans routes for a date from all Approved requests (SCW-F-040 to SCW-F-042)."""
    return route_service.generate_routes(db, data.date)


admin_or_driver = require_roles(UserRole.ADMIN, UserRole.DRIVER)


@router.get("", response_model=list[RouteOut])
def list_routes(
    on_date: date | None = Query(default=None, alias="date"),
    db: Session = Depends(get_db),
    user: User = Depends(admin_or_driver),
):
    """Routes for a date: all of them for an Admin, their own for a driver."""
    return [route_service.describe_route(db, r) for r in route_service.list_routes(db, user, on_date)]


@router.get("/assigned", response_model=list[RouteOut])
def assigned_routes(
    db: Session = Depends(get_db),
    driver: User = Depends(require_roles(UserRole.DRIVER)),
):
    """The logged-in driver's planned and running routes (SCW-F-043)."""
    return [route_service.describe_route(db, r) for r in route_service.assigned_routes(db, driver)]


@router.get("/{route_id}", response_model=RouteOut)
def get_route(route_id: int, db: Session = Depends(get_db), user: User = Depends(admin_or_driver)):
    """One route with its ordered stops."""
    return route_service.describe_route(db, route_service.get_route_for(db, user, route_id))


@router.patch("/{route_id}/stops/{stop_id}", response_model=StopUpdated)
def update_stop(
    route_id: int,
    stop_id: int,
    data: StopUpdate,
    db: Session = Depends(get_db),
    driver: User = Depends(require_roles(UserRole.DRIVER)),
):
    """The route's driver marks a stop Collected or Missed (SCW-F-044)."""
    return route_service.update_stop(db, driver, route_id, stop_id, data.status)
