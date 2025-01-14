from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from models.postgresql import userModel, deviceModel, deviceGestureModel, gestureModel, deviceTypeModel
from schemas.postgresql import userSchemas, utils, deviceSchemas, deviceGestureSchemas, gestureSchemas
from crud.postgresql import utilsCrud
from core.postgresql import database
from sqlalchemy.orm import joinedload

import time


# User queries to test

def selectUsersTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    batch_size = 65000
    start = time.time()

    try:
        for i in range(0, len(id_list), batch_size):
            chunk = id_list[i:i + batch_size]
            chunk_results = db.query(userModel.User).filter(userModel.User.user_id.in_(chunk)).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find user: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def insertUsersTest(user_list: List[userSchemas.UserCreate], db: Session = Depends(database.get_db)):
    if not user_list:
        raise HTTPException(status_code=400, detail="The user_list cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users) + 1);")

    bulk_data = [
        {
            "username": user.username,
            "email": user.email,
            "password_hash": user.password_hash
        }
        for user in user_list
    ]

    start = time.time()

    try:
        db.bulk_insert_mappings(userModel.User, bulk_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create users: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateUsersTest(user_list: List[userSchemas.UserUpdate], db: Session = Depends(database.get_db)):
    if not user_list:
        raise HTTPException(status_code=400, detail="The user_list cannot be empty.")

    users_to_update = []
    for user in user_list:
        db_user = db.query(userModel.User).filter(userModel.User.user_id == user.user_id).first()
        if not db_user:
            raise HTTPException(status_code=400, detail=f"User with id {user.user_id} not found")

        db_user.username = user.username
        db_user.email = user.email
        db_user.password_hash = user.password_hash
        users_to_update.append(db_user)

    start = time.time()

    try:
        db.bulk_save_objects(users_to_update)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update users: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def deleteUsersTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    batch_size = 65000
    start = time.time()

    try:
        for i in range(0, len(id_list), batch_size):
            chunk = id_list[i:i + batch_size]
            db.query(userModel.User).filter(userModel.User.user_id.in_(chunk)).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete users: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


# Devices queries to test

def selectDevicesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    batch_size = 65000
    start = time.time()

    try:
        for i in range(0, len(id_list), batch_size):
            chunk = id_list[i:i + batch_size]
            chunk_results = db.query(deviceModel.Device).options(joinedload(deviceModel.Device.device_gestures)).filter(
                deviceModel.Device.user_id.in_(chunk)
            ).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find device: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def insertDevicesTest(device_list: List[deviceSchemas.DeviceCreate], db: Session = Depends(database.get_db)):
    if not device_list:
        raise HTTPException(status_code=400, detail="The device_list cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('devices_device_id_seq', (SELECT MAX(device_id) FROM devices) + 1);")

    bulk_data = [
        {
            "device_name": device.device_name.lower(),
            "device_type_id": device.device_type_id,
            "user_id": device.user_id
        }
        for device in device_list
    ]

    start = time.time()

    try:
        db.bulk_insert_mappings(deviceModel.Device, bulk_data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create devices: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateDevicesTest(device_list: List[deviceSchemas.DeviceUpdate], db: Session = Depends(database.get_db)):
    if not device_list:
        raise HTTPException(status_code=400, detail="The device_list cannot be empty.")

    devices_to_update = []
    for device in device_list:
        db_device = db.query(deviceModel.Device).filter(deviceModel.Device.device_id == device.device_id).first()
        if not db_device:
            raise HTTPException(status_code=400, detail=f"Device with id {device.device_id} not found")

        db_device.device_name = device.device_name
        db_device.device_type_id = device.device_type_id
        db_device.user_id = device.user_id
        devices_to_update.append(db_device)

    start = time.time()

    try:
        db.bulk_save_objects(devices_to_update)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update devices: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def deleteDevicesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    batch_size = 65000  # Adjust batch size as necessary to avoid hitting the parameter limit
    start = time.time()

    try:
        for i in range(0, len(id_list), batch_size):
            chunk = id_list[i:i + batch_size]
            db.query(deviceModel.Device).filter(deviceModel.Device.device_id.in_(chunk)).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete devices: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


# DeviceGestures queries to test

def selectDeviceGesturesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    batch_size = 65000  # Adjust batch size as necessary to avoid hitting the parameter limit
    results = []

    start = time.time()

    try:
        # Process the id_list in chunks
        for i in range(0, len(id_list), batch_size):
            chunk = id_list[i:i + batch_size]
            chunk_results = db.query(
                deviceGestureModel.DeviceGesture.device_gesture_id,
                deviceGestureModel.DeviceGesture.device_id,
                deviceGestureModel.DeviceGesture.gesture_name,
                gestureModel.Gesture.gesture_id,
                gestureModel.Gesture.gesture_type,
                gestureModel.Gesture.description
            ).join(
                gestureModel.Gesture, deviceGestureModel.DeviceGesture.gesture_id == gestureModel.Gesture.gesture_id
            ).filter(
                deviceGestureModel.DeviceGesture.device_id.in_(chunk)
            ).all()
            # results.extend(chunk_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch device gestures: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def insertDeviceGesturesTest(request: deviceGestureSchemas.DeviceGestureCreateTest,
                             db: Session = Depends(database.get_db)):
    if not request:
        raise HTTPException(status_code=400, detail="The request cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('device_gestures_device_gesture_id_seq', (SELECT MAX(device_gesture_id) FROM device_gestures) + 1);")

    start = time.time()

    try:
        subquery = (
            db.query(deviceModel.Device.device_id)
            .join(deviceTypeModel.DeviceType, deviceModel.Device.device_type_id == deviceTypeModel.DeviceType.device_type_id)
            .filter(deviceTypeModel.DeviceType.type_name == request.device_type_name)
            .subquery()
        )

        devices_exist = db.query(subquery).count()
        if devices_exist == 0:
            raise HTTPException(status_code=404, detail="No devices found for the given device type.")

        bulk_data = [
            {
                "gesture_name": request.gesture_name,
                "gesture_id": request.gesture_id,
                "device_id": row.device_id
            }
            for row in db.query(subquery).all()
        ]

        db.bulk_insert_mappings(deviceGestureModel.DeviceGesture, bulk_data)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create device gestures: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateGestureTest(gesture: gestureSchemas.GestureUpdateByType, db: Session = Depends(database.get_db)):
    if not gesture:
        raise HTTPException(status_code=400, detail="The gesture cannot be empty.")

    db_gesture = db.query(gestureModel.Gesture).filter(
        gestureModel.Gesture.gesture_type == gesture.gesture_type).first()

    start = time.time()

    try:
        db_gesture.description = gesture.description
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update gesture: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def deleteGestureTest(gesture_type: str, db: Session = Depends(database.get_db)):
    if not gesture_type:
        raise HTTPException(status_code=400, detail="The gesture_type cannot be empty.")

    start = time.time()

    try:
        db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_type == gesture_type).delete(
            synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete devices: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time
