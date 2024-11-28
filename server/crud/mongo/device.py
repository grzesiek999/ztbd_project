from bson import ObjectId
from pymongo import UpdateOne
from pymongo.database import Database
from server.schemas.mongo.device import DeviceCreate, DeviceUpdate, DeviceOut
from typing import List


def find_devices(db: Database, user_ids: List[str]) -> List[DeviceOut]:
    devices = db.devices.find({"owner_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}})
    return [DeviceOut(**device) for device in devices]


def insert_devices(db: Database, devices: List[DeviceCreate]) -> List[DeviceOut]:
    device_dicts = [device.model_dump(by_alias=True) for device in devices]
    result = db.devices.insert_many(device_dicts)
    inserted_devices = db.devices.find({"_id": {"$in": result.inserted_ids}})
    return [DeviceOut(**device) for device in inserted_devices]


def update_devices(db: Database, devices: List[DeviceUpdate]) -> List[DeviceOut]:
    bulk_operations = []
    for device in devices:
        update_data = {k: v for k, v in device.model_dump().items() if v is not None}
        bulk_operations.append(
            UpdateOne(
                {"_id": ObjectId(device.id)},
                {"$set": update_data}
            )
        )
    if bulk_operations:
        db.devices.bulk_write(bulk_operations)

    updated_device_ids = [device.id for device in devices]
    updated_devices = db.devices.find({"_id": {"$in": [ObjectId(device_id) for device_id in updated_device_ids]}})
    return [DeviceOut(**device) for device in updated_devices]


def delete_devices(db: Database, device_ids: List[str]):
    db.devices.delete_many({"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}})
