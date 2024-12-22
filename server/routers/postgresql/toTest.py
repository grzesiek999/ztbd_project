from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from schemas.postgresql import userSchemas, utils, deviceSchemas, deviceGestureSchemas
from crud.postgresql import userCrud, deviceCrud, deviceTypeCrud, deviceGestureCrud, utilsCrud
from core.postgresql import database
import time


router = APIRouter(
    prefix="/totest",
    tags=["ToTest"],
)

# Queries to test

@router.get("/get_users_by_id_list")
def get_users_by_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    try:
        userCrud.get_users_by_id_list(db, id_list=id_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.post("/create_users")
def create_users(user_list: List[userSchemas.UserCreate], db: Session = Depends(database.get_db)):

    if not user_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users) + 1);")

    start = time.time()
    for user in user_list:
        try:
            userCrud.create_user(db, user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.patch("/update_users")
def update_users(user_list: List[userSchemas.UserUpdate], db: Session = Depends(database.get_db)):

    if not user_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for user in user_list:
        try:
            userCrud.update_user(db, user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.delete("/delete_users")
def delete_users(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    for uid in id_list:
        try:
            userCrud.delete_user(db, uid)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.get("/get_devices_by_user_id_list")
def get_devices_by_user_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    try:
        deviceCrud.get_devices_by_user_id_list(db, id_list)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find device: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.post("/create_devices")
def create_devices(device_list: List[deviceSchemas.DeviceCreate], db: Session = Depends(database.get_db)):

    if not device_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('devices_device_id_seq', (SELECT MAX(device_id) FROM devices) + 1);")

    start = time.time()
    for device in device_list:
        try:
            deviceCrud.create_device(db, device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create device: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.patch("/update_devices")
def update_devices(device_list: List[deviceSchemas.DeviceUpdate], db: Session = Depends(database.get_db)):

    if not device_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for device in device_list:
        try:
            deviceCrud.update_device(db, device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update device: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.delete("/delete_devices")
def delete_devices(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    for did in id_list:
        try:
            deviceCrud.delete_device(db, did)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.get("/get_device_gestures_by_device_id_list")
def get_device_gestures_by_device_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    try:
        deviceGestureCrud.get_device_gestures_by_device_id_list(db, id_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create device gesture: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.post("/create_devices_gestures")
def create_devices_gestures(device_gesture_list: List[deviceGestureSchemas.DeviceGestureCreate], db: Session = Depends(database.get_db)):

    if not device_gesture_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('device_gestures_device_gesture_id_seq', (SELECT MAX(device_gesture_id) FROM device_gestures) + 1);")

    start = time.time()
    for device_gesture in device_gesture_list:
        try:
            deviceGestureCrud.create_device_gesture(db, device_gesture)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create device gesture: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})

@router.delete("/delete_devices_gestures")
def delete_devices_gestures(gesture_type: str, db: Session = Depends(database.get_db)):

    if not gesture_type:
        raise HTTPException(status_code=400, detail="The gesture_type cannot be empty.")

    start = time.time()
    try:
        deviceGestureCrud.delete_devices_gestures_by_gesture_type(db, gesture_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    end = time.time()
    query_time = (end - start) * 1000

    return JSONResponse(status_code=200, content={"Query Time:": query_time})