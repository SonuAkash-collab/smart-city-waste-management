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
