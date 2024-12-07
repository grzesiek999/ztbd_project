from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from schemas.postgresql import userSchemas
from crud.postgresql import userCrud
from core.postgresql import database
import time


router = APIRouter(
    prefix="/user",
    tags=["user"],
)



@router.get("/get_user_by_id", response_model=userSchemas.User)
def get_user_by_id(uid: int, db: Session = Depends(database.get_db)):

    start = time.time()
    db_user = userCrud.get_user_by_id(db, uid)
    end = time.time()
    print(end - start)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    return db_user


@router.get("/get_user_by_email", response_model=userSchemas.User)
def get_user_by_email(email: str, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    return db_user


@router.get("/get_users_by_name", response_model=List[userSchemas.User])
def get_users_by_name(name: str, db: Session = Depends(database.get_db)):

    db_users = userCrud.get_users_by_name(db, name=name)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found !")

    return db_users


@router.get("/get_users_by_created_at", response_model=List[userSchemas.User])
def fet_users_by_email(created_at: datetime, db: Session =Depends(database.get_db)):

    db_users = userCrud.get_users_by_created_at(db, created_at=created_at)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found !")

    return db_users


@router.post("/create_user", response_model=userSchemas.User)
def create_user(user: userSchemas.UserCreate, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered !")

    return userCrud.create_user(db, user)


@router.patch("/update_user", response_model=userSchemas.User)
def update_user(user: userSchemas.UserUpdate, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, user.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return userCrud.update_user(db, user)


@router.delete("/delete_user")
def delete_user(uid: int, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return userCrud.delete_user(db, uid)