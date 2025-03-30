from sqlalchemy import Column, ForeignKey, String, Text, Integer, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Item(BaseModel):
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # Markdown content
    image = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    is_featured = Column(Boolean, default=False)
    difficulty = Column(String, nullable=True)  # e.g., "Beginner", "Intermediate", "Advanced"
    
    # Relationships
    category = relationship("Category", back_populates="items")
    bookmarks = relationship("Bookmark", back_populates="item", cascade="all, delete-orphan") 