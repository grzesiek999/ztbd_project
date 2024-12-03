from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from pydantic import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBase(BaseModel):
    username: str = Field(..., examples=["Foo"])
    email: EmailStr = Field(..., examples=["johndoe@example.com"])


class UserCreate(UserBase):
    password_hash: str = Field(..., examples=["hashedpassword123"])


class UserOut(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class UserUpdate(BaseModel):
    username: Optional[str] = Field(..., examples=["Foo"])
    email: Optional[EmailStr] = Field(..., examples=["johndoe@example.com"])
    password_hash: Optional[str] = Field(..., examples=["hashedpassword123"])


class UserIDsRequest(BaseModel):
    user_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])


class BulkUserUpdate(BaseModel):
    user_ids: List[str] = Field(..., examples=[["60a5e2e3b8d5f6b8e3f8e5f6", "60a5e2e3b8d5f6b8e3f8e5f7"]])
    update_data: UserUpdate
