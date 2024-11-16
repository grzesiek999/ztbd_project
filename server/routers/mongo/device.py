from typing import List
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from server.schemas.mongo.device import DeviceOut, DeviceCreate, DeviceUpdate
from server.crud.mongo import device as crud_device
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[DeviceOut])
async def read_devices(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device.get_devices(db)


@router.get("/{user_id}/{device_id}", response_model=DeviceOut)
async def read_device(user_id: str, device_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    device = await crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.post("/{user_id}", response_model=DeviceOut)
async def create_device(user_id: str, device_in: DeviceCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device.create_user_device(db, user_id, device_in)


@router.put("/{user_id}/{device_id}", response_model=DeviceOut)
async def update_device(user_id: str, device_id: str, device_in: DeviceUpdate,
                        db: AsyncIOMotorDatabase = Depends(get_db)):
    device = await crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return await crud_device.update_user_device(db, user_id, device_in)


@router.delete("/{user_id}/{device_id}")
async def delete_device(user_id: str, device_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    device = await crud_device.get_device_by_id(db, user_id, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    await crud_device.delete_user_device(db, user_id, device_id)
    return {"detail": "Device deleted"}
