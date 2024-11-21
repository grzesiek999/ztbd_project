from pydantic import BaseModel
from typing import List, Optional
from server.schemas.postgresql.userGestureSchemas import UserGesture


# Device

class DeviceBase(BaseModel):
    device_name: str

class DeviceCreate(DeviceBase):
    user_id: int
    device_type_id: int

class DeviceUpdate(DeviceBase):
    id: int
    device_name: Optional[str] = None
    user_id: Optional[int] = None
    device_type_id: Optional[int] = None

class Device(DeviceBase):
    id: int

    user_gestures: List["UserGesture"] = []

    class Config:
        orm_mode = True