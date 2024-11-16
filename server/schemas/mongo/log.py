from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from pydantic import BeforeValidator
from typing import Annotated

# PyObjectId definition
PyObjectId = Annotated[str, BeforeValidator(str)]


class LogBase(BaseModel):
    user_id: PyObjectId
    gesture_id: PyObjectId
    device_id: str
    timestamp: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


class LogCreate(LogBase):
    pass


class LogOut(LogBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
