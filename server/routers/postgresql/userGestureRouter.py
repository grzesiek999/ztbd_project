from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.schemas.postgresql import userGestureSchemas
from server.crud.postgresql import userCrud, userGestureCrud, deviceCrud, gestureCrud
from server.core import database
from typing import List


router = APIRouter(
    prefix="/usergesture",
    tags=["UserGesture"]
)


@router.get("/get_usergesture_by_id", response_model=userGestureSchemas.UserGesture)
def get_usergesture_by_id(ugid: int, db: Session = Depends(database.get_db)):
    db_usergesture = userGestureCrud.get_usergesture_by_id(db, ugid=ugid)

    if db_usergesture is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_usergesture

@router.get("/get_usergestures_by_user_id", response_model=List[userGestureSchemas.UserGesture])
def get_usergestures_by_user_id(user_id: int, db: Session = Depends(database.get_db)):
    db_usergestures = userGestureCrud.get_usergestures_by_user_id(db, user_id=user_id)

    if db_usergestures is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_usergestures

@router.get("/get_usergestures_by_gesture_id", response_model=List[userGestureSchemas.UserGesture])
def get_usergestures_by_gesture_id(gesture_id: int, db: Session = Depends(database.get_db)):
    db_usergestures = userGestureCrud.get_usergestures_by_gesture_id(db, gesture_id=gesture_id)

    if db_usergestures is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_usergestures

@router.get("/get_usergestures_by_device_id", response_model=List[userGestureSchemas.UserGesture])
def get_usergestures_by_device_id(device_id: int, db: Session = Depends(database.get_db)):
    db_usergestures = userGestureCrud.get_usergestures_by_device_id(db, device_id=device_id)

    if db_usergestures is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return db_usergestures

@router.post("/create_usergesture", response_model=userGestureSchemas.UserGesture)
def create_usergesture(usergesture: userGestureSchemas.UserGestureCreate, db: Session = Depends(database.get_db)):
    db_user = userCrud.get_user_by_id(db, user_id=usergesture.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    db_gesture = gestureCrud.get_gesture_by_id(db, gesture_id=usergesture.gesture_id)
    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    db_device = deviceCrud.get_device_by_id(db, device_id=usergesture.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return userGestureCrud.create_usergesture(db, usergesture=usergesture)

@router.delete("/delete_usergesture")
def delete_usergesture(usergesture_id: int, db: Session = Depends(database.get_db)):
    db_usergesture = userGestureCrud.get_usergesture_by_id(db, ugid=usergesture_id)

    if db_usergesture is None:
        raise HTTPException(status_code=404, detail="UserGesture not found !")

    return userGestureCrud.delete_usergesture(db, usergesture_id=usergesture_id)