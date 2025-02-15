from pydantic import BaseModel
# from typing import List
# from schemas.postgresql.gestureLogsSchemas import GestureLogs


# UserGesture

class DeviceGestureBase(BaseModel):
    gesture_name: str
    gesture_id: int
    device_id: int

class DeviceGestureCreate(DeviceGestureBase):
    pass

class DeviceGesture(DeviceGestureBase):
    device_gesture_id: int
    gesture_name: str

    # gesture_logs: List["GestureLogs"] = []

    class Config:
        from_attributes = True

class DeviceGestureCreateTest(BaseModel):
    device_type_name: str
    gesture_name: str
    gesture_id: int