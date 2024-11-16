from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


async def get_devices_gestures(db: AsyncIOMotorDatabase):
    users = await db.users.find().to_list(1000)
    gestures = []
    for user in users:
        user_id = str(user["_id"])
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("gestures", []):
                gestures.append({**gesture, "user_id": user_id, "device_id": device_id})
    return gestures


async def get_device_gestures_by_user_id(db: AsyncIOMotorDatabase, user_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    gestures = []
    if user:
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("gestures", []):
                gestures.append({**gesture, "device_id": device_id})
    return gestures


async def get_devices_gestures_by_gesture_id(db: AsyncIOMotorDatabase, gesture_id: str):
    users = await db.users.find().to_list(1000)
    gestures = []
    for user in users:
        user_id = str(user["_id"])
        for device in user.get("devices", []):
            device_id = str(device["device_id"])
            for gesture in device.get("gestures", []):
                if gesture["gesture_id"] == ObjectId(gesture_id):
                    gestures.append({**gesture, "user_id": user_id, "device_id": device_id})
    return gestures


async def get_gestures_by_device_id(db: AsyncIOMotorDatabase, user_id: str, device_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for device in user.get("devices", []):
            if device["device_id"] == ObjectId(device_id):
                return device.get("gestures", [])
    return []


async def create_device_gesture(db: AsyncIOMotorDatabase, user_id: str, device_id: str, gesture):
    gesture["gesture_id"] = ObjectId()
    await db.users.update_one(
        {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
        {"$push": {"devices.$.gestures": gesture}}
    )
    return gesture


async def update_device_gesture(db: AsyncIOMotorDatabase, user_id: str, device_id: str, gesture):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for device in user.get("devices", []):
            if device["device_id"] == ObjectId(device_id):
                gestures = device.get("gestures", [])
                for i, existing_gesture in enumerate(gestures):
                    if existing_gesture["gesture_id"] == ObjectId(gesture["gesture_id"]):
                        gestures[i] = {**existing_gesture, **gesture}
                        break
                await db.users.update_one(
                    {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
                    {"$set": {"devices.$.gestures": gestures}}
                )
                return gesture
    return None


async def delete_device_gesture(db: AsyncIOMotorDatabase, user_id: str, device_id: str, gesture_id: str):
    await db.users.update_one(
        {"_id": ObjectId(user_id), "devices.device_id": ObjectId(device_id)},
        {"$pull": {"devices.$.gestures": {"gesture_id": ObjectId(gesture_id)}}}
    )
