from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from typing import Annotated

from schemas.mongo.device_gesture import DeviceGestureBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class DeviceBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    device_type: str
    device_name: str
    owner_id: PyObjectId

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class DeviceCreate(BaseModel):
    device_type: str = Field(..., examples=["Light"])
    device_name: str = Field(..., examples=["Light 1"])
    device_gestures: List[DeviceGestureBase] = Field(default_factory=list)
    owner_id: PyObjectId = Field(..., examples=["60a5e2e3b8d5f6b8e3f8e5f6"])

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class DeviceUpdate(BaseModel):
    device_type: Optional[str] = Field(None, examples=["Light"])
    device_name: Optional[str] = Field(None, examples=["Light 1"])


class DeviceOut(DeviceBase):
    device_gestures: List[DeviceGestureBase] = Field(default_factory=list)


class DeviceIDsRequest(BaseModel):
    device_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])


class UserIDsRequest(BaseModel):
    user_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])


class BulkDeviceUpdate(BaseModel):
    device_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])
    update_data: DeviceUpdate
