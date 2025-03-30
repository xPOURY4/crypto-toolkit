from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Category(BaseModel):
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    
    # Relationships
    items = relationship("Item", back_populates="category", cascade="all, delete-orphan") 