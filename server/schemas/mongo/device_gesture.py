from typing import Optional, List
from pydantic import BaseModel, Field


class DeviceGestureBase(BaseModel):
    gesture_id: str = Field(..., examples=["60a5e2e3b8d5f6b8e3f8e5f6"])
    gesture_type: str = Field(..., examples=["Right Swipe"])
    gesture_name: str = Field(..., examples=["Swipe to the right"])
    gesture_description: str = Field(..., examples=["Swipe right gesture"])


class DeviceGestureCreate(BaseModel):
    gesture_type: str = Field(..., examples=["Right Swipe"])
    gesture_name: str = Field(..., examples=["Swipe to the right"])
    gesture_description: str = Field(..., examples=["Swipe right gesture"])


class DeviceGestureUpdate(BaseModel):
    gesture_type: str = Field(None, examples=["Right Swipe"])
    gesture_description: str = Field(None, examples=["Swipe right gesture update"])


class BulkDeviceGesturesCreate(BaseModel):
    device_type: str = Field(..., examples=["Mobile"])
    gesture: DeviceGestureCreate


class DeviceGestureDeletePattern(BaseModel):
    gesture_type: Optional[str] = Field(None, examples=["Right Swipe"])


class DeviceGestureOut(DeviceGestureBase):
    pass


# class DeviceIDsAndGesturesCreateRequest(BaseModel):
#     device_id: str
#     gesture: DeviceGestureCreate


# class DeviceIDsAndGesturesUpdateRequest(BaseModel):
#     device_id: str
#     gesture: DeviceGestureUpdate
#
#
# class DeviceIDsAndGesturesDeleteRequest(BaseModel):
#     device_id: str
#     gesture_id: str


# class BulkDeviceGesturesCreate(BaseModel):
#     device_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])
#     gesture: DeviceGestureCreate


# class BulkDeviceGesturesUpdate(BaseModel):
#     device_ids: List[str]
#     gesture: DeviceGestureUpdate


# class BulkDeviceGesturesDelete(BaseModel):
#     device_ids: List[str]
#     gesture: DeviceGestureDeletePattern
