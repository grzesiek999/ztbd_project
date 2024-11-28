from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from server.schemas.mongo.user import UserOut, UserCreate, UserUpdate, UserIDsRequest
from server.crud.mongo import user as crud_user
from server.core.mongo.database import get_db

router = APIRouter()


@router.post("/bulk/find", response_model=List[UserOut])
def find_users(request: UserIDsRequest, db: Database = Depends(get_db)):
    return crud_user.find_users(db, request.user_ids)


@router.post("/bulk/insert", response_model=List[UserOut])
def insert_users(users: List[UserCreate], db: Database = Depends(get_db)):
    return crud_user.insert_users(db, users)


@router.put("/bulk/update", response_model=List[UserOut])
def update_users(users: List[UserUpdate], db: Database = Depends(get_db)):
    return crud_user.update_users(db, users)


@router.delete("/bulk/delete")
def delete_users(request: UserIDsRequest, db: Database = Depends(get_db)):
    crud_user.delete_users(db, request.user_ids)
    return {"detail": "Users deleted"}
