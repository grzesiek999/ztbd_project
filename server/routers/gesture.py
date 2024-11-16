from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from server import database, crud
from server.schemas.posrgresql import schemas


router = APIRouter(
    prefix="/gesture",
    tags=["gesture"],
)


@router.get("/get_gesture_by_id", response_model=schemas.Gesture)
def get_gesture_by_id(gid: int, db: Session = Depends(database.get_db)):
    db_gesture = crud.get_gesture_by_id(db, gesture_id=gid)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gesture

@router.get("/get_gestures_by_name", response_model=List[schemas.Gesture])
def get_gestures_by_name(name: str, db: Session = Depends(database.get_db)):
    db_gestures = crud.get_gestures_by_name(db, gesture_name=name)

    if db_gestures is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return db_gestures

@router.post("/create_gesture", response_model=schemas.Gesture)
def create_gesture(gesture: schemas.GestureCreate, db: Session = Depends(database.get_db)):
    return crud.create_gesture(db, gesture=gesture)

@router.patch("/update_gesture", response_model=schemas.Gesture)
def update_gesture(gesture: schemas.GestureUpdate, db: Session = Depends(database.get_db)):
    db_gesture = crud.get_gesture_by_id(db, gesture_id=gesture.id)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return crud.update_gesture(db, gesture=gesture)

@router.delete("/delete_gesture")
def delete_gesture(gid: int, db: Session = Depends(database.get_db)):
    db_gesture = crud.get_gesture_by_id(db, gesture_id=gid)

    if db_gesture is None:
        raise HTTPException(status_code=404, detail="Gesture not found !")

    return crud.delete_gesture(db, gesture_id=gid)