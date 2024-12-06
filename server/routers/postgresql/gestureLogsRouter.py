from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.postgresql import gestureLogsCrud
from schemas.postgresql import  gestureLogsSchemas
from core.postgresql import database

router = APIRouter(
    prefix="/gesture_logs",
    tags=["GestureLogs"],
)



@router.get("/get_gesture_log_by_id", response_model=gestureLogsSchemas.GestureLogs)
def get_gesture_log_by_id(glid: int, db: Session = Depends(database.get_db)):

    db_gesture_log = gestureLogsCrud.get_gesture_log_by_id(db, glid)

    if db_gesture_log is None:
        raise HTTPException(status_code=404, detail="Gesture Log not found !")

    return db_gesture_log