from typing import Optional
from pydantic import BaseModel

from app.schemas.base import BaseSchema
from app.schemas.category import Category


# Shared properties
class ItemBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: Optional[bool] = False
    difficulty: Optional[str] = None


# Properties to receive via API on creation
class ItemCreate(ItemBase):
    name: str
    content: str
    category_id: int


# Properties to receive via API on update
class ItemUpdate(ItemBase):
    pass


# Additional properties to return via API
class Item(BaseSchema, ItemBase):
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True 