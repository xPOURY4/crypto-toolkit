from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Bookmark(BaseModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    item = relationship("Item", back_populates="bookmarks") 