from typing import Optional, List
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
    gesture_id: str
    gesture_name: Optional[str]


class DeviceGestureOut(DeviceGestureBase):
    pass


class DeviceIDsAndGesturesCreateRequest(BaseModel):
    device_id: str
    gesture: DeviceGestureCreate


class DeviceIDsAndGesturesUpdateRequest(BaseModel):
    device_id: str
    gesture: DeviceGestureUpdate


class DeviceIDsAndGesturesDeleteRequest(BaseModel):
    device_id: str
    gesture_id: str
