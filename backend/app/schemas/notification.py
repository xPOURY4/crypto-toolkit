from typing import Optional
from pydantic import BaseModel

from app.schemas.base import BaseSchema


# Shared properties
class NotificationBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_read: Optional[bool] = False
    notification_type: Optional[str] = None
    user_id: Optional[int] = None


# Properties to receive via API on creation
class NotificationCreate(NotificationBase):
    title: str
    content: str
    notification_type: str
    user_id: int


# Properties to receive via API on update
class NotificationUpdate(NotificationBase):
    pass


# Additional properties to return via API
class Notification(BaseSchema, NotificationBase):
    pass 