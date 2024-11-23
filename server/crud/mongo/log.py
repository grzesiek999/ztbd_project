from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
import datetime
from server.models.mongo.log import GestureLog
from server.schemas.mongo.log import LogCreate


def create_gesture_log(db: AsyncIOMotorDatabase, log_in: LogCreate) -> GestureLog:
    log_data = log_in.model_dump()
    log_data["timestamp"] = datetime.datetime.now(datetime.UTC)
    result = db.gesture_logs.insert_one(log_data)
    return GestureLog(**log_data, log_id=result.inserted_id)


def get_gesture_logs(db: AsyncIOMotorDatabase) -> list[GestureLog]:
    logs = []
    for log in db.gesture_logs.find():
        logs.append(GestureLog(**log))
    return logs


def get_gesture_log_by_id(db: AsyncIOMotorDatabase, log_id: str) -> GestureLog | None:
    log = db.gesture_logs.find_one({"_id": ObjectId(log_id)})
    if log:
        return GestureLog(**log)
    return None


def delete_gesture_log(db: AsyncIOMotorDatabase, log_id: str) -> bool:
    result = db.gesture_logs.delete_one({"_id": ObjectId(log_id)})
    return result.deleted_count > 0
