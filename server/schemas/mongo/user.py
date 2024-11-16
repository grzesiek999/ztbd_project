from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

from server.schemas.mongo.device import DeviceBase

PyObjectId = Annotated[str, BeforeValidator(str)]


# class UserGestureBase(BaseModel):
#     gesture_id: str  # uuid.uuid4().hex
#     gesture_name: str
#
#
# class DeviceBase(BaseModel):
#     device_id: str  # uuid.uuid4().hex
#     device_name: str
#     device_type: str
#     user_gestures: List[UserGestureBase] = []


class UserBase(BaseModel):
    username: str
    email: EmailStr
    devices: List[DeviceBase] = []


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    devices: Optional[List[DeviceBase]] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
