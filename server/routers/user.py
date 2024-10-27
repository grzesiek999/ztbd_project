from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from server import schemas, database, crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/get_users_by_name", response_model=List[schemas.User])
def get_users_by_name(name: str, db: Session = Depends(database.get_db)):
    return crud.get_users_by_name(db, name=name)

@router.get("/get_users_by_created_at", response_model=List[schemas.User])
def fet_users_by_email(created_at: datetime, db: Session =Depends(database.get_db)):
    return crud.get_users_by_created_at(db, created_at=created_at)

@router.post("/create_user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.user_email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db=db, user=user)
