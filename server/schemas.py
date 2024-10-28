from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


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
    user_gestures: List["UserGesture"] = []

    class Config:
        orm_mode = True


# Gesture
class GestureBase(BaseModel):
    gesture_name: str
    description: Optional[str] = None

class GestureCreate(GestureBase):
    pass

class GestureUpdate(GestureBase):
    id: int
    gesture_name: Optional[str] = None
    description: Optional[str] = None

class Gesture(GestureBase):
    id: int

    user_gestures: List["UserGesture"] = []

    class Config:
        orm_mode = True


# Device
class DeviceBase(BaseModel):
    device_name: str
    device_type: str

class DeviceCreate(DeviceBase):
    user_id: int

class DeviceUpdate(DeviceBase):
    id: int
    device_name: Optional[str] = None
    device_type: Optional[str] = None

class Device(DeviceBase):
    id: int

    user_gestures: List["UserGesture"] = []

    class Config:
        orm_mode = True


# UserGesture
class UserGestureBase(BaseModel):
    created_at: datetime
    user_id: int
    gesture_id: int
    device_id: int

class UserGestureCreate(UserGestureBase):
    pass

class UserGesture(UserGestureBase):
    id: int

    class Config:
        orm_mode = True
