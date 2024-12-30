from bson import ObjectId
from pymongo.database import Database
from typing import List

from crud.mongo.profiler import get_last_query_time
from schemas.mongo.device_gesture import DeviceGestureOut, DeviceGestureUpdate, BulkDeviceGesturesCreate, \
    DeviceGestureDeletePattern
import time


def find_gestures(db: Database, device_ids: List[str]) -> float:
    # Add 'list' method - to force the query to execute
    start = time.time()
    list(db.devices.find(
        {"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}},
        {"device_gestures": 1, "_id": 0},
        comment="backend_query"
    ))
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


# TODO: Check if working
def find_gestures_by_device_ids(db: Database, device_ids: List[str]):
    start = time.time()
    gestures = db.devices.aggregate([
        {"$match": {"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}}},
        {"$unwind": "$device_gestures"},
        {"$project": {
            "_id": 0,
            "device_id": "$_id",
            "gesture_id": "$device_gestures.gesture_id",
            "gesture_type": "$device_gestures.gesture_type",
            "gesture_name": "$device_gestures.gesture_name",
            "gesture_description": "$device_gestures.gesture_description"
        }}
    ], comment="backend_query")

    gestures_list = list(gestures)  # Convert cursor to list to measure the time accurately
    end = time.time()
    query_time = (end - start) * 1000

    return query_time


# TODO: Check if working
def find_gestures_by_type(db: Database, gesture_type: str) -> float:
    start = time.time()
    list(db.devices.find(
        {"device_gestures.gesture_type": gesture_type},
        {
            "device_gestures.$": 1,  # This projects only the first matched gesture
            "device_name": 1,
            "device_type": 1,
            "owner_id": 1
        }
    ))
    end = time.time()
    query_time = (end - start) * 1000
    return query_time


# def insert_gestures(db: Database, gestures_request: BulkDeviceGesturesCreate) -> int:
#     gesture_data = gestures_request.gesture.model_dump()
#     gesture_data["gesture_id"] = str(ObjectId())
#     device_ids = [ObjectId(device_id) for device_id in gestures_request.device_ids]
#
#     if device_ids and gesture_data:
#         db.devices.update_many(
#             {"_id": {"$in": device_ids}},
#             {"$push": {"device_gestures": gesture_data}},
#             comment="backend_query"
#         )
#     return get_last_query_time(db)


# TODO: Check if working
def insert_gestures_by_device_type(db: Database, gesture_and_devicetype: BulkDeviceGesturesCreate) -> float:
    gesture_data = gesture_and_devicetype.gesture.model_dump()
    gesture_data["gesture_id"] = str(ObjectId())
    device_type = gesture_and_devicetype.device_type

    start = time.time()
    db.devices.update_many(
        {"device_type": device_type},
        {"$push": {"device_gestures": gesture_data}},
        comment="backend_query"
    )
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def update_gestures_by_type(db: Database, gesture: DeviceGestureUpdate) -> float:
    gesture_data = gesture.model_dump()

    start = time.time()
    if gesture_data:
        db.devices.update_many(
            {"device_gestures.gesture_type": gesture_data["gesture_type"]},
            {
                "$set": {
                    "device_gestures.$.gesture_description": gesture_data["gesture_description"]
                }
            },
            comment="backend_query"
        )
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def delete_gestures_by_type(db: Database, gesture: DeviceGestureDeletePattern) -> float:
    gesture_criteria = gesture.model_dump(exclude_unset=True)

    start = time.time()
    if gesture_criteria:
        db.devices.update_many(
            {"device_gestures.gesture_type": gesture_criteria.get("gesture_type")},
            {"$pull": {"device_gestures": {"gesture_type": gesture_criteria.get("gesture_type")}}},
            comment="backend_query"
        )
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)
