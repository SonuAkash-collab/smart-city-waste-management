from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import UserRole
from app.schemas.routes import GenerateResult, GenerateRoutes
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
