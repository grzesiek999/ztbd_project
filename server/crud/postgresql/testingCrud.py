from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.postgresql import userModel, deviceModel, deviceGestureModel, gestureModel
from schemas.postgresql import userSchemas, utils, deviceSchemas, deviceGestureSchemas, gestureSchemas
from crud.postgresql import utilsCrud
from core.postgresql import database
from passlib.context import CryptContext

import time


# User queries to test

def selectUsersTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()

    try:
        db.query(userModel.User).filter(userModel.User.user_id.in_(id_list)).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find user: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def createUsersTest(user_list: List[userSchemas.UserCreate], db: Session = Depends(database.get_db)):
    if not user_list:
        raise HTTPException(status_code=400, detail="The user_list cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users) + 1);")

    db_users = []
    for user in user_list:
        db_user = userModel.User(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash
        )
        db_users.append(db_user)

    start = time.time()

    for db_user in db_users:
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateUsersTest(user_list: List[userSchemas.UserUpdate], db: Session = Depends(database.get_db)):
    if not user_list:
        raise HTTPException(status_code=400, detail="The user_list cannot be empty.")

    start = time.time()

    for user in user_list:
        try:
            db_user = db.query(userModel.User).filter(userModel.User.user_id == user.user_id).first()
            try:
                if user.username is not None:
                    db_user.username = user.username
                if user.email is not None:
                    db_user.email = user.email
                if user.password_hash is not None:
                    db_user.password_hash = user.password_hash
                db.commit()
                db.refresh(db_user)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
        except Exception as err:
            raise HTTPException(status_code=400, detail=f"Failed to find user: {str(err)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def deleteUsersTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()

    for uid in id_list:
        try:
            db.delete(db.query(userModel.User).filter(userModel.User.user_id == uid).first())
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


# Devices queries to test

def selectDevicesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()

    try:
        db.query(deviceModel.Device).filter(deviceModel.Device.user_id.in_(id_list)).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find device: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def createDevicesTest(device_list: List[deviceSchemas.DeviceCreate], db: Session = Depends(database.get_db)):
    if not device_list:
        raise HTTPException(status_code=400, detail="The device_list cannot be empty.")

    utilsCrud.reset_sequence(db, "SELECT setval('devices_device_id_seq', (SELECT MAX(device_id) FROM devices) + 1);")

    db_devices = []
    for device in device_list:
        db_device = deviceModel.Device(
            device_name=device.device_name,
            device_type_id=device.device_type_id,
            user_id=device.user_id
        )
        db_devices.append(db_device)

    start = time.time()

    for db_device in db_devices:
        try:
            db.add(db_device)
            db.commit()
            db.refresh(db_device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create device: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateDevicesTest(device_list: List[deviceSchemas.DeviceUpdate], db: Session = Depends(database.get_db)):
    if not device_list:
        raise HTTPException(status_code=400, detail="The device_list cannot be empty.")

    start = time.time()

    for device in device_list:
        try:
            db_device = db.query(deviceModel.Device).filter(deviceModel.Device.device_id == device.device_id).first()
            try:
                if device.device_name is not None:
                    db_device.device_name = device.device_name.lower()
                if device.device_type_id is not None:
                    db_device.device_type_id = device.device_type_id
                db.commit()
                db.refresh(db_device)
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to update device: {str(e)}")
        except Exception as err:
            raise HTTPException(status_code=400, detail=f"Failed to find device: {str(err)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def deleteDevicesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()

    for did in id_list:
        try:
            db.delete(db.query(deviceModel.Device).filter(deviceModel.Device.device_id == did).first())
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


# DeviceGestures queries to test

def selectDeviceGesturesTest(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()

    try:
        db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.device_id.in_(id_list)).all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to find device gesture: {str(e)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


'''
def createDeviceGesturesTest(device_gesture_list: List[deviceGestureSchemas.DeviceGestureCreate], db: Session = Depends(database.get_db)):

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

    return query_time
'''


def deleteDeviceGesturesTest(gesture_type: str, db: Session = Depends(database.get_db)):
    if not gesture_type:
        raise HTTPException(status_code=400, detail="The gesture_type cannot be empty.")

    start = time.time()

    try:
        gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_type == gesture_type).first()
        try:
            db.query(deviceGestureModel.DeviceGesture).filter(
                deviceGestureModel.DeviceGesture.gesture_id == gesture.gesture_id).delete(synchronize_session=False)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete device gesture: {str(e)}")
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to find gesture: {str(err)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time


def updateGestureTest(gesture: gestureSchemas.GestureUpdateByType, db: Session = Depends(database.get_db)):
    if not gesture:
        raise HTTPException(status_code=400, detail="The gesture cannot be empty.")

    start = time.time()

    try:
        db_gesture = db.query(gestureModel.Gesture).filter(
            gestureModel.Gesture.gesture_type == gesture.gesture_type).first()
        try:
            if gesture.description is not None:
                db_gesture.description = gesture.description
            db.commit()
            db.refresh(db_gesture)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update gesture: {str(e)}")
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Failed to find gesture: {str(err)}")

    end = time.time()
    query_time = (end - start) * 1000

    return query_time
