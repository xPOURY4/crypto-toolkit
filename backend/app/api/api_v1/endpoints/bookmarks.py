from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.bookmark import Bookmark, BookmarkCreate
from app.services import bookmark as bookmark_service
from app.services import item as item_service

router = APIRouter()


@router.get("/", response_model=List[Bookmark])
def read_bookmarks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve current user's bookmarks
    """
    bookmarks = bookmark_service.get_all_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return bookmarks


@router.post("/", response_model=Bookmark)
def create_bookmark(
    *,
    db: Session = Depends(deps.get_db),
    bookmark_in: BookmarkCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bookmark
    """
    # Check if the item exists
    item = item_service.get_by_id(db, item_id=bookmark_in.item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    # Check if bookmark already exists
    existing_bookmark = bookmark_service.get_by_user_and_item(
        db, user_id=current_user.id, item_id=bookmark_in.item_id
    )
    if existing_bookmark:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already bookmarked",
        )
    
    bookmark = bookmark_service.create(db, obj_in=bookmark_in, user=current_user)
    return bookmark


@router.delete("/{bookmark_id}", response_model=Bookmark)
def delete_bookmark(
    *,
    db: Session = Depends(deps.get_db),
    bookmark_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a bookmark
    """
    bookmark = bookmark_service.get_by_id(db, bookmark_id=bookmark_id)
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )
    
    # Ensure user owns the bookmark
    if bookmark.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    bookmark = bookmark_service.delete(db, db_obj=bookmark)
    return bookmark 