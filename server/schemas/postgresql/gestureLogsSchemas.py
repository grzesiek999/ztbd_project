from pydantic import BaseModel
from datetime import datetime
from typing import List


class GestureLogsBase(BaseModel):
    device_gesture_id: int


class GestureLogsCreate(GestureLogsBase):
    pass


class GestureLogs(GestureLogsBase):
    id: int
    created_at: datetime


    class Config:
        orm_mode = True
