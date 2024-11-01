from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import func
from passlib.context import CryptContext
import models, schemas
from datetime import datetime


# User CRUD

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.user_email == email).first()

def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.user_name == name).all()

def get_users_by_created_at(db: Session, created_at: datetime):
    target_date = created_at.date()
    return db.query(models.User).filter(func.date(models.User.created_at) == target_date).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        user_name=user.user_name,
        user_email=user.user_email.lower(),
        password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()

    try:
        if user.user_name is not None:
            db_user.user_name = user.user_name
        if user.user_email is not None:
            db_user.user_email = user.user_email.lower()
        if user.password is not None:
            db_user.password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)

        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User deleted"})


# Gesture CRUD

def get_gesture_by_id(db: Session, gesture_id: int):
    return db.query(models.Gesture).filter(models.Gesture.id == gesture_id).first()

def get_gestures_by_name(db: Session, gesture_name: str):
    return db.query(models.Gesture).filter(models.Gesture.gesture_name == gesture_name).all()

def create_gesture(db: Session, gesture: schemas.GestureCreate):
    db_gesture = models.Gesture(
        gesture_name=gesture.gesture_name.lower(),
        description=gesture.description.lower()
    )

    db.add(db_gesture)
    db.commit()
    db.refresh(db_gesture)
    return db_gesture

def update_gesture(db: Session, gesture: schemas.GestureUpdate):
    db_gesture = db.query(models.Gesture).filter(models.Gesture.id == gesture.id).first()

    try:
        if gesture.gesture_name is not None:
            db_gesture.gesture_name = gesture.gesture_name.lower()
        if gesture.description is not None:
            db_gesture.description = gesture.description.lower()

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture

def delete_gesture(db: Session, gesture_id: int):
    db_gesture = db.query(models.Gesture).filter(models.Gesture.id == gesture_id).first()
    db.delete(db_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Gesture deleted"})


# Device CRUD

def get_device_by_id(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices_by_name(db: Session, device_name: str):
    return db.query(models.Device).filter(models.Device.device_name == device_name).all()

def get_devices_by_type(db: Session, device_type: str):
    return db.query(models.Device).filter(models.Device.device_type == device_type).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(
        device_name =  device.device_name.lower(),
        device_type = device.device_type.lower(),
        user_id = device.user_id
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device: schemas.DeviceUpdate):
    db_device = db.query(models.Device).filter(models.Device.id == device.id).first()

    try:
        if device.device_name is not None:
            db_device.device_name = device.device_name.lower()
        if device.device_type is not None:
            db_device.device_type = device.device_type.lower()

        db.commit()
        db.refresh(db_device)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_device

def delete_device(db: Session, device_id: int):
    db_device = db.query(models.Device).filter(models.Device.id == device_id).first()
    db.delete(db_device)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Device deleted"})


# UserGesture CRUD

def get_usergesture_by_id(db: Session, ugid: int):
    return db.query(models.UserGesture).filter(models.UserGesture.id == ugid).first()

def get_usergestures_by_user_id(db: Session, user_id: int):
    return db.query(models.UserGesture).filter(models.UserGesture.user_id == user_id).all()

def get_usergestures_by_gesture_id(db: Session, gesture_id: int):
    return db.query(models.UserGesture).filter(models.UserGesture.gesture_id == gesture_id).all()

def get_usergestures_by_device_id(db: Session, device_id: int):
    return db.query(models.UserGesture).filter(models.UserGesture.device_id == device_id).all()

def create_usergesture(db: Session, usergesture: schemas.UserGestureCreate):
    db_usergesture = models.UserGesture(
        user_id=usergesture.user_id,
        gesture_id=usergesture.gesture_id,
        device_id=usergesture.device_id
    )
    db.add(db_usergesture)
    db.commit()
    db.refresh(db_usergesture)
    return db_usergesture

def delete_usergesture(db: Session, usergesture_id: int):
    db_usergesture = db.query(models.UserGesture).filter(models.UserGesture.id == usergesture_id).first()
    db.delete(db_usergesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User gesture deleted"})