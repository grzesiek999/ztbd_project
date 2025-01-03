from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserGesture(BaseModel):
    gesture_id: str
    gesture_type: str
    gesture_name: str
    gesture_description: str


class Device(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    device_name: str
    device_type: str
    device_gestures: Optional[List[UserGesture]] = Field(default_factory=list)
    owner_id: PyObjectId

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password_hash": "hashed_password",
                "created_at": "2024-11-14T00:00:00Z"
            }
        }
    )
