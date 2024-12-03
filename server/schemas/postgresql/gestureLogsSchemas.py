from pydantic import BaseModel
from datetime import datetime
from typing import List


class GestureLogsBase(BaseModel):
    device_gesture_id: int


class GestureLogsCreate(GestureLogsBase):
    pass


class GestureLogs(GestureLogsBase):
    log_id: int
    timestamp: datetime


    class Config:
        from_attributes = True
