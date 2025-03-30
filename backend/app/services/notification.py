from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


def get_by_id(db: Session, notification_id: int) -> Optional[Notification]:
    """Get a notification by ID."""
    return db.query(Notification).filter(Notification.id == notification_id).first()


def get_all_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100, unread_only: bool = False) -> List[Notification]:
    """Get all notifications for a user with pagination."""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()


def create(db: Session, obj_in: NotificationCreate) -> Notification:
    """Create a new notification."""
    db_obj = Notification(
        user_id=obj_in.user_id,
        title=obj_in.title,
        content=obj_in.content,
        notification_type=obj_in.notification_type,
        is_read=False,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Notification, obj_in: NotificationUpdate) -> Notification:
    """Update a notification."""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def mark_as_read(db: Session, db_obj: Notification) -> Notification:
    """Mark a notification as read."""
    db_obj.is_read = True
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def mark_all_as_read(db: Session, user_id: int) -> int:
    """Mark all notifications for a user as read."""
    result = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return result


def delete(db: Session, db_obj: Notification) -> Notification:
    """Delete a notification."""
    db.delete(db_obj)
    db.commit()
    return db_obj 