from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server import schemas, database, crud


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

@router.post("/create_gesture", response_model=schemas.Gesture)
def create_gesture(gesture: schemas.GestureCreate, db: Session = Depends(database.get_db)):
    return crud.create_gesture(db, gesture=gesture)