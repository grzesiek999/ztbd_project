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
    gesture_type: str
    gesture_name: str
    gesture_description: str


class DeviceGestureDeletePattern(BaseModel):
    gesture_type: Optional[str]


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


class BulkDeviceGesturesCreate(BaseModel):
    device_ids: List[str]
    gesture: DeviceGestureCreate


class BulkDeviceGesturesUpdate(BaseModel):
    device_ids: List[str]
    gesture: DeviceGestureUpdate


class BulkDeviceGesturesDelete(BaseModel):
    device_ids: List[str]
    gesture: DeviceGestureDeletePattern
