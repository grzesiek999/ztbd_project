from typing import Optional
from pydantic import BaseModel


class DeviceGestureBase(BaseModel):
    gesture_id: str
    gesture_type: str
    gesture_name: str
    gesture_description: str


class DeviceGestureCreate(BaseModel):
    gesture_type: str
    gesture_name: str
    gesture_description: str


class DeviceGestureUpdate(BaseModel):
    gesture_type: Optional[str]
    gesture_name: Optional[str]
    gesture_description: Optional[str]


class DeviceGestureOut(DeviceGestureBase):
    pass
