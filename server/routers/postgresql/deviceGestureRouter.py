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


# Queries to test

@router.get("/get_device_gestures_by_device_id_list", response_model=List[deviceGestureSchemas.DeviceGesture])
def get_device_gestures_by_device_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    db_device_gestures = deviceGestureCrud.get_device_gestures_by_device_id_list(db, id_list)

    if not db_device_gestures:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_device_gestures


@router.post("/create_devices_gestures")
def create_devices_gestures(device_gesture_list: List[deviceGestureSchemas.DeviceGestureCreate], db: Session = Depends(database.get_db)):

    if not device_gesture_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for device_gesture in device_gesture_list:
        try:
            deviceGestureCrud.create_device_gesture(db, device_gesture)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create device gesture: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})