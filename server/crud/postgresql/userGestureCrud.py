from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import userGestureModel
from server.schemas.postgresql import userGestureSchemas


# UserGesture CRUD

def get_usergesture_by_id(db: Session, ugid: int):
    return db.query(userGestureModel.UserGesture).filter(userGestureModel.UserGesture.id == ugid).first()

def get_usergestures_by_user_id(db: Session, user_id: int):
    return db.query(userGestureModel.UserGesture).filter(userGestureModel.UserGesture.user_id == user_id).all()

def get_usergestures_by_gesture_id(db: Session, gesture_id: int):
    return db.query(userGestureModel.UserGesture).filter(userGestureModel.UserGesture.gesture_id == gesture_id).all()

def get_usergestures_by_device_id(db: Session, device_id: int):
    return db.query(userGestureModel.UserGesture).filter(userGestureModel.UserGesture.device_id == device_id).all()

def create_usergesture(db: Session, usergesture: userGestureSchemas.UserGestureCreate):
    db_usergesture = userGestureModel.UserGesture(
        user_id=usergesture.user_id,
        gesture_id=usergesture.gesture_id,
        device_id=usergesture.device_id
    )
    db.add(db_usergesture)
    db.commit()
    db.refresh(db_usergesture)
    return db_usergesture

def delete_usergesture(db: Session, usergesture_id: int):
    db_usergesture = db.query(userGestureModel.UserGesture).filter(userGestureModel.UserGesture.id == usergesture_id).first()
    db.delete(db_usergesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User gesture deleted"})