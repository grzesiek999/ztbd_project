import datetime
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from passlib.hash import bcrypt

from server.models.mongo.user import User
from server.schemas.mongo.user import UserCreate, UserUpdate


async def get_users(db: AsyncIOMotorDatabase) -> List[User]:
    return await db.users.find().to_list(1000)


async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str) -> User:
    return await db.users.find_one({"_id": ObjectId(user_id)})


async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> User:
    return await db.users.find_one({"email": email})


async def get_users_by_created_at(db: AsyncIOMotorDatabase, created_at: str) -> List[User]:
    return await db.users.find({"created_at": created_at}).to_list(1000)


async def create_user(db: AsyncIOMotorDatabase, user: UserCreate) -> User:
    user_dict = user.model_dump()
    user_dict["password"] = bcrypt.using(rounds=13).hash(user.password)
    user_dict["created_at"] = datetime.datetime.now(datetime.UTC)
    new_user = await db.users.insert_one(user_dict)
    created_user = await db.users.find_one({"_id": new_user.inserted_id})
    return created_user


async def update_user(db: AsyncIOMotorDatabase, user_id: str, user: UserUpdate) -> User:
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}
    if "password" in update_data:
        update_data["password"] = bcrypt.using(rounds=13).hash(update_data["password"])
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return await db.users.find_one({"_id": ObjectId(user_id)})


async def delete_user(db: AsyncIOMotorDatabase, user_id: str):
    await db.users.delete_one({"_id": ObjectId(user_id)})
