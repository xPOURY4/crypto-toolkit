from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.bookmark import Bookmark
from app.models.user import User
from app.schemas.bookmark import BookmarkCreate


def get_by_id(db: Session, bookmark_id: int) -> Optional[Bookmark]:
    """Get a bookmark by ID."""
    return db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()


def get_by_user_and_item(db: Session, user_id: int, item_id: int) -> Optional[Bookmark]:
    """Get a bookmark by user ID and item ID."""
    return db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.item_id == item_id,
    ).first()


def get_all_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Bookmark]:
    """Get all bookmarks for a user with pagination."""
    return db.query(Bookmark).filter(
        Bookmark.user_id == user_id
    ).offset(skip).limit(limit).all()


def create(db: Session, obj_in: BookmarkCreate, user: User) -> Bookmark:
    """Create a new bookmark."""
    db_obj = Bookmark(
        user_id=user.id,
        item_id=obj_in.item_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, db_obj: Bookmark) -> Bookmark:
    """Delete a bookmark."""
    db.delete(db_obj)
    db.commit()
    return db_obj 