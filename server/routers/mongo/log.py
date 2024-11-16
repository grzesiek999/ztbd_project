from fastapi import APIRouter, Depends, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase

from server.schemas.mongo.log import LogOut, LogCreate
from server.crud.mongo import log as crud_log
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[LogOut])
async def read_logs(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_log.get_gesture_logs(db)


@router.get("/{log_id}", response_model=LogOut)
async def read_log(log_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    log = await crud_log.get_gesture_log_by_id(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.post("/", response_model=LogOut)
async def create_log(log_in: LogCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_log.create_gesture_log(db, log_in)


@router.delete("/{log_id}")
async def delete_log(log_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    success = await crud_log.delete_gesture_log(db, log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"detail": "Log deleted"}
