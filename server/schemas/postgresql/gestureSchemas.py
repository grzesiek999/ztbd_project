from pydantic import BaseModel
from typing import List, Optional
from server.schemas.postgresql.userGestureSchemas import UserGesture


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

    user_gestures: List["UserGesture"] = []

    class Config:
        orm_mode = True