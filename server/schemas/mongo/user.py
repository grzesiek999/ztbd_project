from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBase(BaseModel):
    username: str
    email: EmailStr


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
    username: Optional[str]
    email: Optional[EmailStr]
    password_hash: Optional[str]


class UserIDsRequest(BaseModel):
    user_ids: List[str]


class BulkUserUpdate(BaseModel):
    user_ids: List[str]
    update_data: UserUpdate
