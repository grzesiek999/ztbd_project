from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from datetime import datetime
from pydantic import BeforeValidator
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]


class GestureLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    gesture_id: str
    timestamp: datetime
    device_id: str

    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True
    )
