from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import User, UserRole
from app.schemas.requests import RequestCreate, RequestCreated
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
