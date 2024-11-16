from typing import Optional
from pydantic import BaseModel


class DeviceGestureBase(BaseModel):
    gesture_id: str  # uuid.uuid4().hex
    gesture_type: str
    gesture_name: str
    description: str


class DeviceGestureCreate(BaseModel):
    gesture_type: str
    gesture_name: str
    description: str


class DeviceGestureUpdate(BaseModel):
    gesture_type: Optional[str]
    gesture_name: Optional[str]
    description: Optional[str]


class DeviceGestureOut(DeviceGestureBase):
    pass
