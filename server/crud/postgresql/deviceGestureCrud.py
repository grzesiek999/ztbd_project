from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import deviceGestureModel
from server.schemas.postgresql import deviceGestureSchemas


# UserGesture CRUD

def get_device_gesture_by_id(db: Session, dgid: int):
    return db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.id == dgid).first()

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
    db_device_gesture = db.query(deviceGestureModel.DeviceGesture).filter(deviceGestureModel.DeviceGesture.id == dgid).first()
    db.delete(db_device_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User gesture deleted"})