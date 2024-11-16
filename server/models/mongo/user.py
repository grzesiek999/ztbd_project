from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserGesture(BaseModel):
    gesture_id: str  # uuid.uuid4().hex
    gesture_type: str
    gesture_name: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class Device(BaseModel):
    device_id: str  # uuid.uuid4().hex
    device_name: str
    device_type: str
    user_gestures: Optional[List[UserGesture]] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    password_hash: str
    created_at: datetime
    devices: List[Device] = []

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password_hash": "hashed_password",
                "created_at": "2024-11-14T00:00:00Z",
                "devices": [
                    {
                        "device_id": "device_id_1",
                        "device_name": "Device A",
                        "device_type": "Smartphone",
                        "user_gestures": [{"gesture_id": "gesture_id_1", "gesture_name": "swipe_up"}]
                    }
                ]
            }
        }
    )
