"""In-app and email notifications (SCW-F-050)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.notification import Notification
from app.models.user import User
from app.services.mailer import send_email


def notify(db: Session, user_id: int, message: str, email: bool = True) -> Notification:
    """Store an in-app notification and email the same text to the user."""
    notification = Notification(user_id=user_id, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    user = db.get(User, user_id)
    if email and user is not None:
        send_email(user.email, "Smart City Waste: update", message)
    return notification


def list_for(db: Session, user: User, unread_only: bool = False, limit: int = 50) -> tuple[list[Notification], int]:
    query = select(Notification).where(Notification.user_id == user.id)
    if unread_only:
        query = query.where(Notification.is_read.is_(False))
    items = db.scalars(query.order_by(Notification.id.desc()).limit(limit)).all()
    unread = db.query(Notification).filter_by(user_id=user.id, is_read=False).count()
    return list(items), unread


def mark_read(db: Session, user: User, notification_id: int) -> Notification:
    notification = db.get(Notification, notification_id)
    if notification is None or notification.user_id != user.id:
        raise ApiError(404, "NOTIFICATION_NOT_FOUND", "Notification not found.")
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def mark_all_read(db: Session, user: User) -> int:
    changed = db.query(Notification).filter_by(user_id=user.id, is_read=False).update({"is_read": True})
    db.commit()
    return changed
