"""
Crypto Toolkit - A comprehensive educational platform for cryptocurrencies
Copyright (c) 2025 xPOURY4
MIT License
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.services import user as user_service
from app.services import category as category_service
from app.services import item as item_service
from app.services import bookmark as bookmark_service
from app.services import notification as notification_service

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
def read_statistics(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Get system statistics (admin only)
    """
    total_users = len(user_service.get_all(db))
    total_active_users = len([u for u in user_service.get_all(db) if u.is_active])
    
    total_categories = len(category_service.get_all(db))
    total_items = len(item_service.get_all(db))
    
    # Get most bookmarked items
    all_items = item_service.get_all(db)
    item_bookmark_counts = {}
    for item in all_items:
        item_bookmark_counts[item.id] = len(item.bookmarks)
    
    top_bookmarked = sorted(
        [(item_id, count) for item_id, count in item_bookmark_counts.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    top_bookmarked_items = []
    for item_id, count in top_bookmarked:
        item = item_service.get_by_id(db, item_id)
        if item:
            top_bookmarked_items.append({
                "id": item.id,
                "name": item.name,
                "bookmark_count": count
            })
    
    return {
        "user_statistics": {
            "total_users": total_users,
            "total_active_users": total_active_users,
            "admin_count": len([u for u in user_service.get_all(db) if u.role == "admin"]),
            "member_count": len([u for u in user_service.get_all(db) if u.role == "member"]),
        },
        "content_statistics": {
            "total_categories": total_categories,
            "total_items": total_items,
            "featured_items": len([i for i in all_items if i.is_featured]),
        },
        "engagement_statistics": {
            "total_bookmarks": len(bookmark_service.get_all_by_user(db, current_user.id)),
            "total_notifications": len(notification_service.get_all_by_user(db, current_user.id)),
            "unread_notifications": len(notification_service.get_all_by_user(db, current_user.id, unread_only=True)),
        },
        "top_bookmarked_items": top_bookmarked_items
    } 