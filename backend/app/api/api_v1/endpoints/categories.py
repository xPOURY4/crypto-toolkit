from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services import category as category_service

router = APIRouter()


@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve categories
    """
    categories = category_service.get_all(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: CategoryCreate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Create new category (admin only)
    """
    category = category_service.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A category with this name already exists",
        )
    
    category = category_service.create(db, obj_in=category_in)
    return category


@router.get("/{category_id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get category by ID
    """
    category = category_service.get_by_id(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: CategoryUpdate,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Update a category (admin only)
    """
    category = category_service.get_by_id(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # If name is being updated, check for duplicates
    if category_in.name and category_in.name != category.name:
        existing_category = category_service.get_by_name(db, name=category_in.name)
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A category with this name already exists",
            )
    
    category = category_service.update(db, db_obj=category, obj_in=category_in)
    return category


@router.delete("/{category_id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Delete a category (admin only)
    """
    category = category_service.get_by_id(db, category_id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # Check if category has items before deletion
    if category.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a category that has items. Move or delete the items first.",
        )
    
    category = category_service.delete(db, db_obj=category)
    return category 