from bson import ObjectId
from pymongo.database import Database
from typing import List

from server.crud.mongo.profiler import get_last_query_time
from server.schemas.mongo.device_gesture import DeviceGestureOut, DeviceGestureUpdate, BulkDeviceGesturesCreate, \
    DeviceGestureDeletePattern


def find_gestures(db: Database, device_ids: List[str]) -> int:
    list(db.devices.find(
        {"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}},
        {"device_gestures": 1, "_id": 0},
        comment="backend_query"
    ))
    return get_last_query_time(db)


def find_gestures_by_ids(db: Database, gesture_ids: List[str]) -> List[DeviceGestureOut]:
    gestures = db.devices.aggregate([
        {"$unwind": "$device_gestures"},
        {"$match": {"device_gestures.gesture_id": {"$in": [ObjectId(gesture_id) for gesture_id in gesture_ids]}}},
        {"$project": {
            "gesture_id": "$device_gestures.gesture_id",
            "gesture_type": "$device_gestures.gesture_type",
            "gesture_name": "$device_gestures.gesture_name",
            "gesture_description": "$device_gestures.gesture_description"
        }}
    ], comment="backend_query")
    return [DeviceGestureOut(**gesture) for gesture in gestures]


def insert_gestures(db: Database, gestures_request: BulkDeviceGesturesCreate) -> int:
    gesture_data = gestures_request.gesture.model_dump()
    gesture_data["gesture_id"] = str(ObjectId())
    device_ids = [ObjectId(device_id) for device_id in gestures_request.device_ids]

    if device_ids and gesture_data:
        db.devices.update_many(
            {"_id": {"$in": device_ids}},
            {"$push": {"device_gestures": gesture_data}},
            comment="backend_query"
        )
    return get_last_query_time(db)


def update_gestures(db: Database, gesture: DeviceGestureUpdate) -> int:
    gesture_data = gesture.model_dump()

    if gesture_data:
        db.devices.update_many(
            {"device_gestures.gesture_type": gesture_data["gesture_type"]},
            {
                "$set": {
                    "device_gestures.$.gesture_name": gesture_data["gesture_name"],
                    "device_gestures.$.gesture_description": gesture_data["gesture_description"]
                }
            },
            comment="backend_query"
        )
    return get_last_query_time(db)


def delete_gestures(db: Database, gesture: DeviceGestureDeletePattern) -> int:
    gesture_criteria = gesture.model_dump(exclude_unset=True)

    if gesture_criteria:
        db.devices.update_many(
            {"device_gestures.gesture_type": gesture_criteria.get("gesture_type")},
            {"$pull": {"device_gestures": {"gesture_type": gesture_criteria.get("gesture_type")}}},
            comment="backend_query"
        )
    return get_last_query_time(db)
