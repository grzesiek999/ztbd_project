from datetime import datetime, timezone
from typing import List

from pymongo import UpdateOne
from pymongo.database import Database

from crud.mongo.profiler import get_last_query_time
from schemas.mongo.user import UserCreate, UserUpdate
from bson import ObjectId
import time


def find_users(db: Database, user_ids: List[str]) -> float:
    start = time.time()
    # Add 'list' method - to force the query to execute
    users = list(db.users.find({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                       comment="backend_query"))
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def insert_users(db: Database, users: List[UserCreate]) -> float:
    user_dicts = []
    for user in users:
        user_data = user.model_dump()
        user_data["created_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        user_dicts.append(user_data)

    start = time.time()
    users = db.users.insert_many(user_dicts, comment="backend_query")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def update_users(db: Database, users_update_data: List[UserUpdate]) -> float:
    updates = []
    for user in users_update_data:
        user_data = user.model_dump(exclude_unset=True)
        user_id = user_data.pop('id')
        if user_data:
            updates.append(
                UpdateOne(
                    {"_id": ObjectId(user_id)},
                    {"$set": user_data}
                )
            )

    start = time.time()
    if updates:
        users = db.users.bulk_write(updates, comment="backend_query")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def delete_users(db: Database, user_ids: List[str]) -> float:
    start = time.time()
    users = db.users.delete_many({"_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                         comment="backend_query")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)
