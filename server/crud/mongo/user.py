from datetime import datetime, timezone
from typing import List

from pymongo import UpdateOne
from pymongo.database import Database
from server.schemas.mongo.user import UserCreate, UserUpdate, UserOut
from bson import ObjectId


def find_users(db: Database, user_ids: List[str]) -> List[UserOut]:
    users = db.users.find({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}})
    return [UserOut(**user) for user in users]


def insert_users(db: Database, users: List[UserCreate]) -> List[UserOut]:
    user_dicts = []
    for user in users:
        user_data = user.model_dump()
        user_data["created_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        user_dicts.append(user_data)
    result = db.users.insert_many(user_dicts)
    return [UserOut(**user) for user in user_dicts]


def update_users(db: Database, users: List[UserUpdate]) -> List[UserOut]:
    bulk_operations = []
    for user in users:
        user_id = user.id
        update_data = user.model_dump(exclude_unset=True, exclude={"id"})
        bulk_operations.append(
            UpdateOne(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
        )

    if bulk_operations:
        db.users.bulk_write(bulk_operations)

    updated_user_ids = [user.id for user in users]
    updated_users = db.users.find({"_id": {"$in": [ObjectId(user_id) for user_id in updated_user_ids]}})
    return [UserOut(**user) for user in updated_users]


def delete_users(db: Database, user_ids: List[str]):
    db.users.delete_many({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}})
