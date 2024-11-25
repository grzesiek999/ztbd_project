from pydantic import BaseModel
from typing import List, Optional
from server.schemas.postgresql.deviceGestureSchemas import DeviceGesture


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

    device_gestures: List["DeviceGesture"] = []

    class Config:
        orm_mode = True