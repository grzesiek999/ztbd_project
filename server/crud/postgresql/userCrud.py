from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import func
from passlib.context import CryptContext
from server.models.postgresql import userModel
from server.schemas.postgresql import userSchemas
from datetime import datetime


# User CRUD

def get_user_by_id(db: Session, user_id: int):
    return db.query(userModel.User).filter(userModel.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(userModel.User).filter(userModel.User.user_email == email).first()

def get_users_by_name(db: Session, name: str):
    return db.query(userModel.User).filter(userModel.User.user_name == name).all()

def get_users_by_created_at(db: Session, created_at: datetime):
    target_date = created_at.date()
    return db.query(userModel.User).filter(func.date(userModel.User.created_at) == target_date).all()

def create_user(db: Session, user: userSchemas.UserCreate):
    db_user = user.User(
        user_name=user.user_name,
        user_email=user.user_email.lower(),
        password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: userSchemas.UserUpdate):
    db_user = db.query(user.User).filter(user.User.id == user.id).first()

    try:
        if user.user_name is not None:
            db_user.user_name = user.user_name
        if user.user_email is not None:
            db_user.user_email = user.user_email.lower()
        if user.password is not None:
            db_user.password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)

        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(userModel.User).filter(userModel.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User deleted"})