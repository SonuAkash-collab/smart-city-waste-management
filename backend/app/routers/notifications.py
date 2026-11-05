from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db import get_db
from app.models.user import User
from app.schemas.notifications import NotificationList, NotificationOut
from app.services import notifications as notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationList)
def my_notifications(unread: bool = False, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """The logged-in user's notifications, newest first."""
    items, count = notification_service.list_for(db, user, unread_only=unread)
    return {"items": items, "unread": count}


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return notification_service.mark_read(db, user, notification_id)


@router.post("/read-all")
def mark_all_read(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"updated": notification_service.mark_all_read(db, user)}
