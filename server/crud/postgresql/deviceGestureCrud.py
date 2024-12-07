from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.postgresql import deviceGestureModel
from schemas.postgresql import deviceGestureSchemas
from typing import List


# UserGesture CRUD

def get_device_gesture_by_id(db: Session, dgid: int):
    return db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.device_gesture_id == dgid).first()

def get_device_gestures_by_gesture_id(db: Session, gid: int):
    return db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.gesture_id == gid).all()

def get_device_gestures_by_device_id(db: Session, did: int):
    return db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.device_id == did).all()

def create_device_gesture(db: Session, deviceGesture: deviceGestureSchemas.DeviceGestureCreate):
    db_device_gesture = deviceGesture.DeviceGesture(
        gesture_name=deviceGesture.gesture_name,
        gesture_id=deviceGesture.gesture_id,
        device_id=deviceGesture.device_id
    )
    db.add(db_device_gesture)
    db.commit()
    db.refresh(db_device_gesture)
    return db_device_gesture

def delete_device_gesture(db: Session, dgid: int):
    db_device_gesture = db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.device_gesture_id == dgid).first()
    db.delete(db_device_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User gesture deleted"})

def get_device_gestures_by_device_id_list(db: Session, id_list: List[int]):
    return db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.device_id.in_(id_list)).all()