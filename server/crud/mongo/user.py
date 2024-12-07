from datetime import datetime, timezone
from typing import List

from pymongo.database import Database

from crud.mongo.profiler import get_last_query_time
from schemas.mongo.user import UserCreate, BulkUserUpdate
from bson import ObjectId


def find_users(db: Database, user_ids: List[str]) -> int:
    list(db.users.find({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                       comment="backend_query"))
    return get_last_query_time(db)


def insert_users(db: Database, users: List[UserCreate]) -> int:
    user_dicts = []
    for user in users:
        user_data = user.model_dump()
        user_data["created_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        user_dicts.append(user_data)
    db.users.insert_many(user_dicts,
                         comment="backend_query")
    return get_last_query_time(db)


def update_users(db: Database, users_update_data: BulkUserUpdate) -> int:
    users_update_data = users_update_data.model_dump()
    user_ids = [ObjectId(user_id) for user_id in users_update_data["user_ids"]]
    update_data = users_update_data["update_data"] if users_update_data[
        "update_data"] else {}

    if user_ids and update_data:
        db.users.update_many(
            {"_id": {"$in": user_ids}},
            {"$set": update_data},
            comment="backend_query"
        )
    return get_last_query_time(db)


def delete_users(db: Database, user_ids: List[str]) -> int:
    db.users.delete_many({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                         comment="backend_query")
    return get_last_query_time(db)
