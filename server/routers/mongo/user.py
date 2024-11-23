from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from server.schemas.mongo.user import UserOut, UserCreate, UserUpdate
from server.crud.mongo import user as crud_user
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[UserOut])
def read_users(db: Database = Depends(get_db)):
    return crud_user.get_users(db)


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, db: Database = Depends(get_db)):
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Database = Depends(get_db)):
    return crud_user.create_user(db, user_in)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_in: UserUpdate, db: Database = Depends(get_db)):
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update_user(db, user_id, user_in)


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Database = Depends(get_db)):
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, user_id)
    return {"detail": "User deleted"}
