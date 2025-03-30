from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services import item as item_service
from app.services import category as category_service
from app.utils.files import save_upload_file

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None,
    difficulty: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items with filtering
    """
    items = item_service.get_all(
        db, 
        skip=skip, 
        limit=limit, 
        category_id=category_id,
        search=search,
        is_featured=is_featured,
        difficulty=difficulty,
    )
    return items


@router.post("/", response_model=Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: ItemCreate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new item (admin only)
    """
    # Verify that the category exists
    category = category_service.get_by_id(db, category_id=item_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    item = item_service.create(db, obj_in=item_in)
    return item


@router.get("/{item_id}", response_model=Item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID
    """
    item = item_service.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update an item (admin only)
    """
    item = item_service.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    # If updating category, verify that it exists
    if item_in.category_id is not None and item_in.category_id != item.category_id:
        category = category_service.get_by_id(db, category_id=item_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
    
    item = item_service.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}", response_model=Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete an item (admin only)
    """
    item = item_service.get_by_id(db, item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    
    item = item_service.delete(db, db_obj=item)
    return item 