from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, Field, ConfigDict
from typing import Annotated

from server.schemas.mongo.device_gesture import DeviceGestureBase

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
    device_type: str
    device_name: str
    device_gestures: List[DeviceGestureBase] = Field(default_factory=list)
    owner_id: PyObjectId

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class DeviceUpdate(BaseModel):
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    # device_gestures: Optional[List[DeviceGestureBase]] = Field(default_factory=list)


class DeviceOut(DeviceBase):
    device_gestures: List[DeviceGestureBase] = Field(default_factory=list)


class DeviceIDsRequest(BaseModel):
    device_ids: List[str]


class UserIDsRequest(BaseModel):
    user_ids: List[str]


class BulkDeviceUpdate(BaseModel):
    device_ids: List[str]
    update_data: DeviceUpdate
