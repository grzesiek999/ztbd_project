from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional
from server.schemas.postgresql.deviceSchemas import Device


# User

class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    created_at: datetime
    devices: List["Device"] = []

    class Config:
        orm_mode = True