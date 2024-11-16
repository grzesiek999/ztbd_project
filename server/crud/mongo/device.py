from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


async def get_devices(db: AsyncIOMotorDatabase):
    users = await db.users.find().to_list(1000)
    devices = []
    for user in users:
        user_devices = user.get("devices", [])
        for device in user_devices:
            devices.append({**device, "user_id": str(user["_id"])})
    return devices


async def get_device_by_id(db: AsyncIOMotorDatabase, user_id: str, device_id: str):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        for device in user.get("devices", []):
            if device["device_id"] == ObjectId(device_id):
                return device
    return None


async def create_user_device(db: AsyncIOMotorDatabase, user_id: str, device):
    device["device_id"] = ObjectId()
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$push": {"devices": device}})
    return device


async def update_user_device(db: AsyncIOMotorDatabase, user_id: str, device):
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        devices = user.get("devices", [])
        for i, existing_device in enumerate(devices):
            if existing_device["device_id"] == ObjectId(device["device_id"]):
                devices[i] = {**existing_device, **device}
                break
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"devices": devices}})
        return device
    return None


async def delete_user_device(db: AsyncIOMotorDatabase, user_id: str, device_id: str):
    await db.users.update_one({"_id": ObjectId(user_id)}, {"$pull": {"devices": {"device_id": ObjectId(device_id)}}})
