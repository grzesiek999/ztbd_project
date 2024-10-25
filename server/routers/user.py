from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models import User
from ..schemas import UserCreate
from ..crud import get_user_by_email
from ..database import get_db



router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create_user", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.user_email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(db=db, user=user)
