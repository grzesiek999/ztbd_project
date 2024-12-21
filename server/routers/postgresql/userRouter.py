from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from schemas.postgresql import userSchemas, utils
from crud.postgresql import userCrud
from core.postgresql import database
import time


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# Get user by id
@router.get("/get_user_by_id", response_model=userSchemas.User)
def get_user_by_id(uid: int, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, uid)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    return db_user

# Get user by email
@router.get("/get_user_by_email", response_model=userSchemas.User)
def get_user_by_email(email: str, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    return db_user

# Get users by name
@router.get("/get_users_by_name", response_model=List[userSchemas.User])
def get_users_by_name(name: str, db: Session = Depends(database.get_db)):

    db_users = userCrud.get_users_by_name(db, name=name)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found !")

    return db_users

# Get users by created date
@router.get("/get_users_by_created_at", response_model=List[userSchemas.User])
def fet_users_by_email(created_at: datetime, db: Session =Depends(database.get_db)):

    db_users = userCrud.get_users_by_created_at(db, created_at=created_at)
    if db_users is None:
        raise HTTPException(status_code=404, detail="Users not found !")

    return db_users

# Create user
@router.post("/create_user", response_model=userSchemas.User)
def create_user(user: userSchemas.UserCreate, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered !")

    return userCrud.create_user(db, user)

# Update user
@router.patch("/update_user", response_model=userSchemas.User)
def update_user(user: userSchemas.UserUpdate, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, user.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return userCrud.update_user(db, user)

# delete user
@router.delete("/delete_user")
def delete_user(uid: int, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, uid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return userCrud.delete_user(db, uid)


# Queries to test

@router.get("/get_users_by_id_list")
def get_users_by_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    db_users = userCrud.get_users_by_id_list(db, id_list=id_list)
    end = time.time()
    query_time = end - start

    if not db_users:
        raise HTTPException(status_code=404, detail="No users found for the provided IDs.")

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.post("/create_users")
def create_users(user_list: List[userSchemas.UserCreate], db: Session = Depends(database.get_db)):

    if not user_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for user in user_list:
        try:
            userCrud.create_user(db, user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.patch("/update_users")
def create_users(user_list: List[userSchemas.UserUpdate], db: Session = Depends(database.get_db)):

    if not user_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for user in user_list:
        try:
            userCrud.update_user(db, user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})