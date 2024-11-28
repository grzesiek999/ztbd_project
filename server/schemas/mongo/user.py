from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

from server.schemas.mongo.device import DeviceBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBase(BaseModel):
    username: str
    email: EmailStr
    # devices: List[DeviceBase] = Field(default_factory=list)


class UserCreate(UserBase):
    password_hash: str


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class UserUpdate(BaseModel):
    id: PyObjectId
    username: Optional[str]
    email: Optional[EmailStr]
    password_hash: Optional[str]
    # devices: Optional[List[DeviceBase]] = Field(default_factory=list)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class UserIDsRequest(BaseModel):
    user_ids: List[str]
