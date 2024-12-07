from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
# from schemas.postgresql.deviceSchemas import Device


# User

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password_hash: str

class UserUpdate(UserBase):
    user_id: int
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None

class User(UserBase):
    user_id: int
    created_at: datetime
    # devices: List["Device"] = []

    class Config:
        from_attributes = True