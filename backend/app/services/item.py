from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_by_id(db: Session, item_id: int) -> Optional[Item]:
    """Get an item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()


def get_all(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    is_featured: Optional[bool] = None,
    difficulty: Optional[str] = None,
) -> List[Item]:
    """Get all items with filtering and pagination."""
    query = db.query(Item)
    
    # Apply filters
    if category_id:
        query = query.filter(Item.category_id == category_id)
    
    if search:
        query = query.filter(
            or_(
                Item.name.ilike(f"%{search}%"),
                Item.description.ilike(f"%{search}%"),
                Item.content.ilike(f"%{search}%"),
            )
        )
    
    if is_featured is not None:
        query = query.filter(Item.is_featured == is_featured)
        
    if difficulty:
        query = query.filter(Item.difficulty == difficulty)
    
    # Apply pagination and return results
    return query.order_by(Item.name).offset(skip).limit(limit).all()


def create(db: Session, obj_in: ItemCreate) -> Item:
    """Create a new item."""
    db_obj = Item(
        name=obj_in.name,
        description=obj_in.description,
        content=obj_in.content,
        image=obj_in.image,
        category_id=obj_in.category_id,
        is_featured=obj_in.is_featured,
        difficulty=obj_in.difficulty,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Item, obj_in: ItemUpdate) -> Item:
    """Update an item."""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, db_obj: Item) -> Item:
    """Delete an item."""
    db.delete(db_obj)
    db.commit()
    return db_obj 