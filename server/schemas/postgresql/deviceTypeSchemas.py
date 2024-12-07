from pydantic import BaseModel
from typing import List, Optional
# from schemas.postgresql.deviceSchemas import Device


class DeviceTypeBase(BaseModel):
    type_name: str


class DeviceTypeCreate(DeviceTypeBase):
    pass


class DeviceTypeUpdate(DeviceTypeBase):
    device_type_id: int
    type_name: Optional[str] = None


class DeviceType(DeviceTypeBase):
    device_type_id: int

    # devices: List["Device"] = []

    class Config:
        from_attributes = True