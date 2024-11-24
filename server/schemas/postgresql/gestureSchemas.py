from pydantic import BaseModel
from typing import List, Optional
from server.schemas.postgresql.deviceGestureSchemas import DeviceGesture


# Gesture

class GestureBase(BaseModel):
    gesture_type: str
    description: Optional[str] = None

class GestureCreate(GestureBase):
    pass

class GestureUpdate(GestureBase):
    id: int
    gesture_type: Optional[str] = None
    description: Optional[str] = None

class Gesture(GestureBase):
    id: int

    device_gestures: List["DeviceGesture"] = []

    class Config:
        orm_mode = True