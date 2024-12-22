from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.postgresql import gestureSchemas
from crud.postgresql import gestureCrud
from core.postgresql import database

router = APIRouter(
    prefix="/gesture",
    tags=["gesture"],
)



@router.get("/get_gesture_by_id", response_model=gestureSchemas.Gesture)
def get_gesture_by_id(gid: int, db: Session = Depends(database.get_db)):

    db_gesture = gestureCrud.get_gesture_by_id(db, gid)
    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gesture


@router.get("/get_gestures_by_type", response_model=List[gestureSchemas.Gesture])
def get_gesture_by_type(type: str, db: Session = Depends(database.get_db)):

    db_gestures = gestureCrud.get_gesture_by_type(db, type)
    if db_gestures is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gestures


@router.post("/create_gesture", response_model=gestureSchemas.Gesture)
def create_gesture(gesture: gestureSchemas.GestureCreate, db: Session = Depends(database.get_db)):

    db_gesture = gestureCrud.get_gesture_by_type(db, gesture.gesture_type)
    if db_gesture:
        raise HTTPException(status_code=409, detail="Gesture already exists")

    return gestureCrud.create_gesture(db, gesture=gesture)


@router.patch("/update_gesture", response_model=gestureSchemas.Gesture)
def update_gesture(gesture: gestureSchemas.GestureUpdate, db: Session = Depends(database.get_db)):

    db_gesture = gestureCrud.get_gesture_by_id(db, gesture.gesture_id)
    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return gestureCrud.update_gesture(db, gesture=gesture)


@router.delete("/delete_gesture")
def delete_gesture(gid: int, db: Session = Depends(database.get_db)):

    db_gesture = gestureCrud.get_gesture_by_id(db, gid)
    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return gestureCrud.delete_gesture(db, gid)


# Query to test

#@router.patch("/up")