from pydantic import BaseModel
from datetime import datetime


# UserGesture

class UserGestureBase(BaseModel):
    user_id: int
    gesture_id: int
    device_id: int

class UserGestureCreate(UserGestureBase):
    pass

class UserGesture(UserGestureBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True