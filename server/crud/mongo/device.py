from bson import ObjectId
from pymongo.database import Database

from crud.mongo.profiler import get_last_query_time
from schemas.mongo.device import DeviceCreate, BulkDeviceUpdate
from typing import List


def find_devices(db: Database, user_ids: List[str]) -> int:
    list(db.devices.find({"owner_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                         comment="backend_query"))
    return get_last_query_time(db)


def insert_devices(db: Database, devices: List[DeviceCreate]) -> int:
    device_dicts = [device.model_dump(by_alias=True) for device in devices]
    db.devices.insert_many(device_dicts,
                           comment="backend_query")
    return get_last_query_time(db)


def update_devices(db: Database, devices_update_data: BulkDeviceUpdate) -> int:
    devices_update_data = devices_update_data.model_dump()
    device_ids = [ObjectId(device_id) for device_id in devices_update_data["device_ids"]]
    update_data = devices_update_data["update_data"] if devices_update_data["update_data"] else {}

    if device_ids and update_data:
        db.devices.update_many(
            {"_id": {"$in": device_ids}},
            {"$set": update_data},
            comment="backend_query"
        )
    return get_last_query_time(db)


def delete_devices(db: Database, device_ids: List[str]) -> int:
    db.devices.delete_many({"_id": {"$in": [ObjectId(device_id) for device_id in device_ids]}},
                           comment="backend_query")
    return get_last_query_time(db)
