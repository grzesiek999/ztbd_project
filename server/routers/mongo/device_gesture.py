from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from schemas.mongo.device import DeviceIDsRequest
from schemas.mongo.device_gesture import DeviceGestureUpdate, BulkDeviceGesturesCreate, \
    DeviceGestureDeletePattern
from crud.mongo import device_gesture as crud_device_gesture
from core.mongo.database import get_db

router = APIRouter()


@router.post("/bulk/find", response_model=float)
def find_gestures(device_ids_request: DeviceIDsRequest, db: Database = Depends(get_db)):
    return crud_device_gesture.find_gestures_by_device_ids(db, device_ids_request.device_ids)


@router.post("/bulk/insert", response_model=float)
def insert_gestures(gesture_and_devicetype: BulkDeviceGesturesCreate, db: Database = Depends(get_db)):
    return crud_device_gesture.insert_gestures_by_device_type(db, gesture_and_devicetype)


@router.put("/bulk/update", response_model=float)
def update_gestures(gestures_request: DeviceGestureUpdate, db: Database = Depends(get_db)):
    return crud_device_gesture.update_gestures_by_type(db, gestures_request)


@router.delete("/bulk/delete", response_model=float)
def delete_gestures(gestures_request: DeviceGestureDeletePattern, db: Database = Depends(get_db)):
    return crud_device_gesture.delete_gestures_by_type(db, gestures_request)
