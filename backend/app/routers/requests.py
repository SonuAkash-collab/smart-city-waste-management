from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.core.deps import get_current_user
from app.models.collection_request import Priority, RequestStatus, WasteType
from app.models.user import User, UserRole
from app.schemas.requests import RequestCreate, RequestCreated, RequestPage
from app.services import requests as request_service

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestCreated, status_code=status.HTTP_201_CREATED)
def submit_request(
    data: RequestCreate,
    db: Session = Depends(get_db),
    citizen: User = Depends(require_roles(UserRole.CITIZEN)),
):
    """Citizen submits a collection request (SCW-F-010)."""
    return request_service.create_request(db, citizen, data)


@router.get("", response_model=RequestPage)
def list_requests(
    status_filter: RequestStatus | None = Query(default=None, alias="status"),
    priority: Priority | None = None,
    waste_type: WasteType | None = Query(default=None, alias="wasteType"),
    on_date: date | None = Query(default=None, alias="date"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Admins filter all requests; Citizens list their own (SCW-F-012, SCW-F-014)."""
    items, total = request_service.list_requests(
        db, user, status_filter, priority, waste_type, on_date, page, size
    )
    return {"items": items, "page": page, "size": size, "total": total}
