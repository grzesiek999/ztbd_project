from pydantic import BaseModel
from typing import List, Optional
# from schemas.postgresql.deviceGestureSchemas import DeviceGesture


# Gesture

class GestureBase(BaseModel):
    gesture_type: str
    description: Optional[str] = None

class GestureCreate(GestureBase):
    pass

class GestureUpdate(GestureBase):
    gesture_id: int
    gesture_type: Optional[str] = None
    description: Optional[str] = None

class GestureUpdateByType(GestureBase):
    pass

class Gesture(GestureBase):
    gesture_id: int

    # device_gestures: List["DeviceGesture"] = []

    class Config:
        from_attributes = True