from typing import List, Optional
from pydantic import BaseModel

from server.schemas.mongo.device_gesture import DeviceGestureBase


# class Gesture(BaseModel):
#     gesture_id: str  # uuid.uuid4().hex
#     gesture_type: str
#     gesture_name: str


class DeviceBase(BaseModel):
    device_id: str  # uuid.uuid4().hex
    device_type: str
    device_name: str


class DeviceCreate(BaseModel):
    device_type: str
    device_name: str
    gestures: List[DeviceGestureBase] = []


class DeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    gestures: Optional[List[DeviceGestureBase]] = []


class DeviceOut(DeviceBase):
    gestures: List[DeviceGestureBase] = []
