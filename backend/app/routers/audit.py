from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import User, UserRole
from app.schemas.audit import AuditEntry
from app.services.audit import list_entries

router = APIRouter(prefix="/audit", tags=["audit"], dependencies=[Depends(require_roles(UserRole.ADMIN))])


@router.get("", response_model=list[AuditEntry])
def read_audit_log(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db)):
    """Latest Admin actions, newest first (SCW-SEC-006)."""
    entries = list_entries(db, limit)
    names = {u.id: u.full_name for u in db.query(User).filter(User.id.in_({e.user_id for e in entries}))}
    return [{**AuditEntry.model_validate(e).model_dump(), "actor_name": names.get(e.user_id)} for e in entries]
