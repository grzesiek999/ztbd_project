from pydantic import BaseModel
from typing import List, Optional
from schemas.postgresql.deviceGestureSchemas import DeviceGesture


# Device

class DeviceBase(BaseModel):
    device_name: str

class DeviceCreate(DeviceBase):
    user_id: int
    device_type_id: int

class DeviceUpdate(DeviceBase):
    device_id: int
    device_name: Optional[str] = None
    user_id: Optional[int] = None
    device_type_id: Optional[int] = None

class Device(DeviceBase):
    device_id: int
    user_id: int
    device_type_id: int

    # device_gestures: List["DeviceGesture"] = []

    class Config:
        from_attributes = True