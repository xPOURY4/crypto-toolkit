from typing import Optional
from pydantic import BaseModel

from app.schemas.base import BaseSchema


# Shared properties
class CategoryBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    name: str


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


# Additional properties to return via API
class Category(BaseSchema, CategoryBase):
    pass 