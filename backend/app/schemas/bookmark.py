from typing import Optional
from pydantic import BaseModel

from app.schemas.base import BaseSchema
from app.schemas.item import Item
from app.schemas.user import User


# Shared properties
class BookmarkBase(BaseModel):
    user_id: Optional[int] = None
    item_id: Optional[int] = None


# Properties to receive via API on creation
class BookmarkCreate(BookmarkBase):
    item_id: int


# Additional properties to return via API
class Bookmark(BaseSchema, BookmarkBase):
    item: Optional[Item] = None
    
    class Config:
        from_attributes = True 