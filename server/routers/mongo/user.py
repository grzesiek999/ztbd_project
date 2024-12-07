from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from schemas.mongo.user import UserCreate, UserIDsRequest, BulkUserUpdate
from crud.mongo import user as crud_user
from core.mongo.database import get_db

router = APIRouter()


@router.post("/bulk/find", response_model=int)
def find_users(request: UserIDsRequest, db: Database = Depends(get_db)):
    return crud_user.find_users(db, request.user_ids)


@router.post("/bulk/insert", response_model=int)
def insert_users(users: List[UserCreate], db: Database = Depends(get_db)):
    return crud_user.insert_users(db, users)


@router.put("/bulk/update", response_model=int)
def update_users(users: BulkUserUpdate, db: Database = Depends(get_db)):
    return crud_user.update_users(db, users)


@router.delete("/bulk/delete", response_model=int)
def delete_users(request: UserIDsRequest, db: Database = Depends(get_db)):
    return crud_user.delete_users(db, request.user_ids)
