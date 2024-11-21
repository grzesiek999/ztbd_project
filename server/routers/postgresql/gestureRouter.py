from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server.schemas.postgresql import gestureSchemas
from server.services.postgresql import gestureCrud
from server.core import database

router = APIRouter(
    prefix="/gesture",
    tags=["gesture"],
)


@router.get("/get_gesture_by_id", response_model=gestureSchemas.Gesture)
def get_gesture_by_id(gid: int, db: Session = Depends(database.get_db)):
    db_gesture = gestureCrud.get_gesture_by_id(db, gesture_id=gid)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gesture

@router.get("/get_gestures_by_name", response_model=List[gestureSchemas.Gesture])
def get_gestures_by_name(name: str, db: Session = Depends(database.get_db)):
    db_gestures = gestureCrud.get_gestures_by_name(db, gesture_name=name)

    if db_gestures is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gestures

@router.post("/create_gesture", response_model=gestureSchemas.Gesture)
def create_gesture(gesture: gestureSchemas.GestureCreate, db: Session = Depends(database.get_db)):
    return gestureCrud.create_gesture(db, gesture=gesture)

@router.patch("/update_gesture", response_model=gestureSchemas.Gesture)
def update_gesture(gesture: gestureSchemas.GestureUpdate, db: Session = Depends(database.get_db)):
    db_gesture = gestureCrud.get_gesture_by_id(db, gesture_id=gesture.id)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return gestureCrud.update_gesture(db, gesture=gesture)

@router.delete("/delete_gesture")
def delete_gesture(gid: int, db: Session = Depends(database.get_db)):
    db_gesture = gestureCrud.get_gesture_by_id(db, gesture_id=gid)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return gestureCrud.delete_gesture(db, gesture_id=gid)