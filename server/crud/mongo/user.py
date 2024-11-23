import datetime
from typing import List
from bson import ObjectId
from pymongo.database import Database
from passlib.hash import bcrypt

from server.models.mongo.user import User
from server.schemas.mongo.user import UserCreate, UserUpdate


def get_users(db: Database) -> List[User]:
    return db.users.find().to_list(1000)


def get_user_by_id(db: Database, user_id: str) -> User:
    return db.users.find_one({"_id": ObjectId(user_id)})


def get_user_by_email(db: Database, email: str) -> User:
    return db.users.find_one({"email": email})


def get_users_by_created_at(db: Database, created_at: str) -> List[User]:
    return db.users.find({"created_at": created_at}).to_list(1000)


def create_user(db: Database, user: UserCreate) -> User:
    user_dict = user.model_dump()
    user_dict["password"] = bcrypt.using(rounds=13).hash(user.password)
    user_dict["created_at"] = datetime.datetime.now(datetime.UTC)
    new_user = db.users.insert_one(user_dict)
    created_user = db.users.find_one({"_id": new_user.inserted_id})
    return created_user


def update_user(db: Database, user_id: str, user: UserUpdate) -> User:
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}
    if "password" in update_data:
        update_data["password"] = bcrypt.using(rounds=13).hash(update_data["password"])
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return db.users.find_one({"_id": ObjectId(user_id)})


def delete_user(db: Database, user_id: str):
    db.users.delete_one({"_id": ObjectId(user_id)})
