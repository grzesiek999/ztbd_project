from typing import List
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from server.schemas.mongo.device_gesture import DeviceGestureOut, DeviceGestureCreate, DeviceGestureUpdate
from server.crud.mongo import device_gesture as crud_device_gesture
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[DeviceGestureOut])
async def read_gestures(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.get_devices_gestures(db)


@router.get("/user/{user_id}", response_model=List[DeviceGestureOut])
async def read_user_gestures(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.get_device_gestures_by_user_id(db, user_id)


@router.get("/gesture/{gesture_id}", response_model=List[DeviceGestureOut])
async def read_gestures_by_gesture_id(gesture_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.get_devices_gestures_by_gesture_id(db, gesture_id)


@router.get("/device/{user_id}/{device_id}", response_model=List[DeviceGestureOut])
async def read_gestures_by_device_id(user_id: str, device_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.get_gestures_by_device_id(db, user_id, device_id)


@router.post("/{user_id}/{device_id}", response_model=DeviceGestureOut)
async def create_gesture(user_id: str, device_id: str, gesture_in: DeviceGestureCreate,
                         db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.create_device_gesture(db, user_id, device_id, gesture_in)


@router.put("/{user_id}/{device_id}", response_model=DeviceGestureOut)
async def update_gesture(user_id: str, device_id: str, gesture_in: DeviceGestureUpdate,
                         db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_device_gesture.update_device_gesture(db, user_id, device_id, gesture_in)


@router.delete("/{user_id}/{device_id}/{gesture_id}")
async def delete_gesture(user_id: str, device_id: str, gesture_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    await crud_device_gesture.delete_device_gesture(db, user_id, device_id, gesture_id)
    return {"detail": "Gesture deleted"}
