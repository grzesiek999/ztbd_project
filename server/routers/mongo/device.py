from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from server.schemas.mongo.device import DeviceOut, DeviceCreate, DeviceUpdate, DeviceIDsRequest, UserIDsRequest
from server.crud.mongo import device as crud_device
from server.core.mongo.database import get_db

router = APIRouter()


@router.post("/bulk/find", response_model=List[DeviceOut])
def find_devices(request: UserIDsRequest, db: Database = Depends(get_db)):
    return crud_device.find_devices(db, request.user_ids)


@router.post("/bulk/insert", response_model=List[DeviceOut])
def insert_devices(devices: List[DeviceCreate], db: Database = Depends(get_db)):
    return crud_device.insert_devices(db, devices)


@router.put("/bulk/update", response_model=List[DeviceOut])
def update_devices(devices: List[DeviceUpdate], db: Database = Depends(get_db)):
    return crud_device.update_devices(db, devices)


@router.delete("/bulk/delete")
def delete_devices(request: DeviceIDsRequest, db: Database = Depends(get_db)):
    crud_device.delete_devices(db, request.device_ids)
    return {"detail": "Devices deleted"}
