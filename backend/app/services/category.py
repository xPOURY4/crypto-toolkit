from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_by_id(db: Session, category_id: int) -> Optional[Category]:
    """Get a category by ID."""
    return db.query(Category).filter(Category.id == category_id).first()


def get_by_name(db: Session, name: str) -> Optional[Category]:
    """Get a category by name."""
    return db.query(Category).filter(Category.name == name).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    """Get all categories with pagination."""
    return db.query(Category).order_by(Category.name).offset(skip).limit(limit).all()


def create(db: Session, obj_in: CategoryCreate) -> Category:
    """Create a new category."""
    db_obj = Category(
        name=obj_in.name,
        description=obj_in.description,
        icon=obj_in.icon,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    """Update a category."""
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_obj, key, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, db_obj: Category) -> Category:
    """Delete a category."""
    db.delete(db_obj)
    db.commit()
    return db_obj 