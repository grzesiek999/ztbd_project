from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.postgresql import deviceGestureSchemas, utils
from crud.postgresql import deviceGestureCrud, deviceCrud, gestureCrud
from core.postgresql import database
from typing import List
import time


router = APIRouter(
    prefix="/devicegesture",
    tags=["DeviceGesture"]
)


@router.get("/get_device_gesture_by_id", response_model=deviceGestureSchemas.DeviceGesture)
def get_device_gesture_by_id(dgid: int, db: Session = Depends(database.get_db)):
    db_device_gesture = deviceGestureCrud.get_device_gesture_by_id(db, dgid=dgid)

    if db_device_gesture is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_device_gesture


@router.get("/get_device_gestures_by_gesture_id", response_model=List[deviceGestureSchemas.DeviceGesture])
def get_device_gestures_by_gesture_id(gid: int, db: Session = Depends(database.get_db)):
    db_device_gestures = deviceGestureCrud.get_device_gestures_by_gesture_id(db, gid)

    if db_device_gestures is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_device_gestures


@router.get("/get_device_gestures_by_device_id", response_model=List[deviceGestureSchemas.DeviceGesture])
def get_device_gestures_by_device_id(did: int, db: Session = Depends(database.get_db)):
    db_device_gestures = deviceGestureCrud.get_device_gestures_by_device_id(db, did)

    if db_device_gestures is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_device_gestures


@router.post("/create_device_gesture", response_model=deviceGestureSchemas.DeviceGesture)
def create_device_gesture(deviceGesture: deviceGestureSchemas.DeviceGestureCreate, db: Session = Depends(
    database.get_db)):
    db_gesture = gestureCrud.get_gesture_by_id(db, deviceGesture.gesture_id)
    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    db_device = deviceCrud.get_device_by_id(db, deviceGesture.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return deviceGestureCrud.create_device_gesture(db, deviceGesture)


@router.delete("/delete_device_gesture")
def delete_device_gesture(dgid: int, db: Session = Depends(database.get_db)):
    db_device_gesture = deviceGestureCrud.get_device_gesture_by_id(db, dgid)

    if db_device_gesture is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return deviceGestureCrud.delete_device_gesture(db, dgid)