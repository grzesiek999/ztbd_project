from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from server.schemas.mongo.device import DeviceOut, DeviceCreate, DeviceUpdate
from server.crud.mongo import device as crud_device
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[DeviceOut])
def read_devices(db: Database = Depends(get_db)):
    return crud_device.get_devices(db)


@router.get("/{user_id}/{device_id}", response_model=DeviceOut)
def read_device(user_id: str, device_id: str, db: Database = Depends(get_db)):
    device = crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/{user_id}", response_model=DeviceOut)
def create_device(user_id: str, device_in: DeviceCreate, db: Database = Depends(get_db)):
    return crud_device.create_user_device(db, user_id, device_in)


@router.put("/{user_id}/{device_id}", response_model=DeviceOut)
def update_device(user_id: str, device_id: str, device_in: DeviceUpdate,
                        db: Database = Depends(get_db)):
    device = crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return crud_device.update_user_device(db, user_id, device_in)


@router.delete("/{user_id}/{device_id}")
def delete_device(user_id: str, device_id: str, db: Database = Depends(get_db)):
    device = crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    crud_device.delete_user_device(db, user_id, device_id)
    return {"detail": "Device deleted"}
