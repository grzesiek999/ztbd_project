from bson import ObjectId
from pymongo.database import Database


def get_devices_gestures(db: Database):
    users = db.users.find().to_list(1000)
    gestures = []
    for user in users:
        user_id = str(user["_id"])
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("device_gestures", []):
                gestures.append({**gesture, "user_id": user_id, "device_id": device_id})
    return gestures


def get_device_gestures_by_user_id(db: Database, user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    gestures = []
    if user:
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("gestures", []):
                gestures.append({**gesture, "device_id": device_id})
    return gestures


def get_devices_gestures_by_gesture_id(db: Database, gesture_id: str):
    users = db.users.find().to_list(1000)
    gestures = []
    for user in users:
        user_id = str(user["_id"])
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("gestures", []):
                if gesture["gesture_id"] == ObjectId(gesture_id):
                    gestures.append({**gesture, "user_id": user_id, "device_id": device_id})
    return gestures


def get_gestures_by_device_id(db: Database, user_id: str, device_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for device in user.get("devices", []):
            if device["device_id"] == ObjectId(device_id):
                return device.get("gestures", [])
    return []


def create_device_gesture(db: Database, user_id: str, device_id: str, gesture):
    gesture["gesture_id"] = ObjectId()
    db.users.update_one(
        {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
        {"$push": {"devices.$.gestures": gesture}}
    )
    return gesture


def update_device_gesture(db: Database, user_id: str, device_id: str, gesture):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for device in user.get("devices", []):
            if device["device_id"] == ObjectId(device_id):
                gestures = device.get("gestures", [])
                for i, existing_gesture in enumerate(gestures):
                    if existing_gesture["gesture_id"] == ObjectId(gesture["gesture_id"]):
                        gestures[i] = {**existing_gesture, **gesture}
                        break
                db.users.update_one(
                    {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
                    {"$set": {"devices.$.gestures": gestures}}
                )
                return gesture
    return None


def delete_device_gesture(db: Database, user_id: str, device_id: str, gesture_id: str):
    db.users.update_one(
        {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
        {"$pull": {"devices.$.gestures": {"gesture_id": ObjectId(gesture_id)}}}
    )
