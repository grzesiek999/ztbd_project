from bson import ObjectId
from pymongo import UpdateOne
from pymongo.database import Database
from typing import List

from server.schemas.mongo.device_gesture import DeviceGestureOut, DeviceIDsAndGesturesCreateRequest, \
    DeviceIDsAndGesturesUpdateRequest, DeviceIDsAndGesturesDeleteRequest, DeviceGestureUpdate


def find_gestures(db: Database, device_ids: List[str]) -> List[DeviceGestureOut]:
    gestures = db.devices.aggregate([
        {"$match": {"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}}},
        {"$unwind": "$device_gestures"},
        {"$project": {
            "gesture_id": "$device_gestures.gesture_id",
            "gesture_type": "$device_gestures.gesture_type",
            "gesture_name": "$device_gestures.gesture_name",
            "gesture_description": "$device_gestures.gesture_description"
        }}
    ])
    return [DeviceGestureOut(**gesture) for gesture in gestures]


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
    ])
    return [DeviceGestureOut(**gesture) for gesture in gestures]


def insert_gestures(db: Database, gestures_request: List[DeviceIDsAndGesturesCreateRequest]) -> List[DeviceGestureOut]:
    bulk_operations = []
    added_gestures = []
    for request in gestures_request:
        request = request.model_dump()
        device_id = request["device_id"]
        gesture = request["gesture"]
        gesture["gesture_id"] = str(ObjectId())
        bulk_operations.append(
            UpdateOne(
                {"_id": ObjectId(device_id)},
                {"$push": {"device_gestures": gesture}}
            )
        )
        added_gestures.append(DeviceGestureOut(**gesture))
    if bulk_operations:
        db.devices.bulk_write(bulk_operations)
    return added_gestures


def update_gestures(db: Database, gestures_request: List[DeviceIDsAndGesturesUpdateRequest]) -> List[DeviceGestureUpdate]:
    bulk_operations = []
    added_gestures = []
    for request in gestures_request:
        request = request.model_dump()
        device_id = request["device_id"]
        gesture = request["gesture"]
        bulk_operations.append(
            UpdateOne(
                {"_id": ObjectId(device_id), "device_gestures.gesture_id": gesture["gesture_id"]},
                {"$set": {"device_gestures.$.gesture_name": gesture["gesture_name"]}}
            )
        )
        added_gestures.append(DeviceGestureUpdate(**gesture))
    if bulk_operations:
        db.devices.bulk_write(bulk_operations)
    return added_gestures


def delete_gestures(db: Database, gestures_request: List[DeviceIDsAndGesturesDeleteRequest]):
    bulk_operations = []
    for request in gestures_request:
        request = request.model_dump()
        device_id = request["device_id"]
        gesture_id = request["gesture_id"]
        bulk_operations.append(
            UpdateOne(
                {"_id": ObjectId(device_id)},
                {"$pull": {"device_gestures": {"gesture_id": gesture_id}}}
            )
        )
    if bulk_operations:
        db.devices.bulk_write(bulk_operations)
    return {"message": "Gestures deleted successfully"}
