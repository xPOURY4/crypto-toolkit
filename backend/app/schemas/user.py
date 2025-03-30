from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.models.user import UserRole
from app.schemas.base import BaseSchema


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = True
    profile_image: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.MEMBER


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Additional properties to return via API
class User(BaseSchema, UserBase):
    pass


# Additional properties stored in DB
class UserInDB(User):
    hashed_password: str 