from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pymongo.database import Database

from schemas.mongo.log import LogOut, LogCreate
from crud.mongo import log as crud_log
from core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[LogOut])
def read_logs(db: Database = Depends(get_db)):
    return crud_log.get_gesture_logs(db)


@router.get("/{log_id}", response_model=LogOut)
def read_log(log_id: str, db: Database = Depends(get_db)):
    log = crud_log.get_gesture_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.post("/", response_model=LogOut)
def create_log(log_in: LogCreate, db: Database = Depends(get_db)):
    return crud_log.create_gesture_log(db, log_in)


@router.delete("/{log_id}")
def delete_log(log_id: str, db: Database = Depends(get_db)):
    success = crud_log.delete_gesture_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"detail": "Log deleted"}
