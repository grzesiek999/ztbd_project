from pydantic import BaseModel
from typing import List, Optional
from server.models.postgresql.deviceModel import Device


class DeviceTypeBase(BaseModel):
    type_name: str


class DeviceTypeCreate(DeviceTypeBase):
    pass


class DeviceTypeUpdate(DeviceTypeBase):
    id: int
    type_name: Optional[str] = None


class DeviceType(DeviceTypeBase):
    id: int

    devices: List["Device"] = []

    class Config:
        orm_mode = True