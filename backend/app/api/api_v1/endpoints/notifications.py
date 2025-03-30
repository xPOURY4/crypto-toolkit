from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.notification import Notification, NotificationCreate, NotificationUpdate
from app.services import notification as notification_service
from app.services import user as user_service

router = APIRouter()


@router.get("/", response_model=List[Notification])
def read_notifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve current user's notifications
    """
    notifications = notification_service.get_all_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit, unread_only=unread_only
    )
    return notifications


@router.post("/", response_model=Notification)
def create_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_in: NotificationCreate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new notification (admin only)
    """
    # Verify that the target user exists
    user = user_service.get_by_id(db, user_id=notification_in.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    notification = notification_service.create(db, obj_in=notification_in)
    return notification


@router.get("/mark-all-read", response_model=dict)
def mark_all_notifications_read(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark all notifications as read for current user
    """
    count = notification_service.mark_all_as_read(db, user_id=current_user.id)
    return {"success": True, "marked_count": count}


@router.get("/{notification_id}", response_model=Notification)
def read_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get notification by ID
    """
    notification = notification_service.get_by_id(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    # Ensure user owns the notification
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return notification


@router.put("/{notification_id}", response_model=Notification)
def update_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    notification_in: NotificationUpdate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update a notification (admin only)
    """
    notification = notification_service.get_by_id(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    notification = notification_service.update(db, db_obj=notification, obj_in=notification_in)
    return notification


@router.put("/{notification_id}/read", response_model=Notification)
def mark_notification_read(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a notification as read
    """
    notification = notification_service.get_by_id(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    # Ensure user owns the notification
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    notification = notification_service.mark_as_read(db, db_obj=notification)
    return notification


@router.delete("/{notification_id}", response_model=Notification)
def delete_notification(
    *,
    db: Session = Depends(deps.get_db),
    notification_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a notification
    """
    notification = notification_service.get_by_id(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    
    # Only allow admins or the notification owner to delete it
    if notification.user_id != current_user.id and not user_service.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    notification = notification_service.delete(db, db_obj=notification)
    return notification 