from os import device_encoding

from bson import ObjectId
from pymongo import UpdateOne
from pymongo.database import Database
from pymongo.errors import PyMongoError

from crud.mongo.profiler import get_last_query_time
from schemas.mongo.device import DeviceCreate, DeviceUpdate
from typing import List
import time


def find_devices(db: Database, user_ids: List[str]) -> float:
    # Add 'list' method - to force the query to execute
    start = time.time()
    devices = list(db.devices.find({"owner_id": {"$in": [ObjectId(user_id) for user_id in user_ids]}},
                         comment="backend_query"))
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def insert_devices(db: Database, devices: List[DeviceCreate]) -> float:
    device_dicts = [device.model_dump(by_alias=True) for device in devices]
    for device_dict in device_dicts:
        device_dict['device_gestures'] = []
    start = time.time()
    devices = db.devices.insert_many(device_dicts,
                           comment="backend_query")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def update_devices(db: Database, devices_update_data: List[DeviceUpdate]) -> float:
    updates = []
    for device in devices_update_data:
        device_data = device.model_dump(exclude_unset=True)
        device_id = device_data.pop('id')
        device_data['owner_id'] = ObjectId(device_data['owner_id'])
        if device_data:
            updates.append(
                UpdateOne(
                    {"_id": ObjectId(device_id)},
                    {"$set": device_data}
                )
            )

    start = time.time()
    if updates:
        devices = db.devices.bulk_write(updates, comment="backend_query")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)


def delete_devices(db: Database, device_ids: List[str]) -> float:
    batch_size = 250000

    start = time.time()
    try:
        # Przetwarzanie urządzeń w partiach
        for i in range(0, len(device_ids), batch_size):
            chunk = device_ids[i:i + batch_size]
            result = db.devices.delete_many(
                {"_id": {"$in": [ObjectId(device_id) for device_id in chunk]}},
                comment="backend_query"
            )
    except PyMongoError as e:
        raise RuntimeError(f"Failed to delete devices: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000
    return query_time
    # return get_last_query_time(db)
