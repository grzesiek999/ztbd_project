from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from server.schemas.mongo.device import DeviceIDsRequest
from server.schemas.mongo.device_gesture import DeviceGestureOut, DeviceIDsAndGesturesCreateRequest, \
    DeviceIDsAndGesturesUpdateRequest, DeviceIDsAndGesturesDeleteRequest, DeviceGestureUpdate
from server.crud.mongo import device_gesture as crud_device_gesture
from server.core.mongo.database import get_db

router = APIRouter()


@router.post("/bulk/find", response_model=List[DeviceGestureOut])
def find_gestures(device_ids_request: DeviceIDsRequest, db: Database = Depends(get_db)):
    return crud_device_gesture.find_gestures(db, device_ids_request.device_ids)


@router.post("/bulk/insert", response_model=List[DeviceGestureOut])
def insert_gestures(gestures_request: List[DeviceIDsAndGesturesCreateRequest], db: Database = Depends(get_db)):
    return crud_device_gesture.insert_gestures(db, gestures_request)


@router.put("/bulk/update", response_model=List[DeviceGestureUpdate])
def update_gestures(gestures_request: List[DeviceIDsAndGesturesUpdateRequest], db: Database = Depends(get_db)):
    return crud_device_gesture.update_gestures(db, gestures_request)


@router.delete("/bulk/delete")
def delete_gestures(gestures_request: List[DeviceIDsAndGesturesDeleteRequest], db: Database = Depends(get_db)):
    return crud_device_gesture.delete_gestures(db, gestures_request)
