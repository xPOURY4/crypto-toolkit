from sqlalchemy import Column, ForeignKey, String, Text, Integer, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Notification(BaseModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    notification_type = Column(String, nullable=False)  # e.g., "system", "item", "update"
    
    # Relationships
    user = relationship("User", back_populates="notifications") 