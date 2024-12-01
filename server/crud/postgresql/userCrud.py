from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import func
from passlib.context import CryptContext
from server.models.postgresql import userModel
from server.schemas.postgresql import userSchemas
from datetime import datetime


# User CRUD

def get_user_by_id(db: Session, uid: int):
    return db.query(userModel.User).filter(userModel.User.user_id == uid).first()

def get_user_by_email(db: Session, email: str):
    return db.query(userModel.User).filter(userModel.User.email == email).first()

def get_users_by_name(db: Session, name: str):
    return db.query(userModel.User).filter(userModel.User.username == name).all()

def get_users_by_created_at(db: Session, created_at: datetime):
    target_date = created_at.date()
    return db.query(userModel.User).filter(func.date(userModel.User.created_at) == target_date).all()

def create_user(db: Session, user: userSchemas.UserCreate):
    db_user = user.User(
        username=user.username,
        email=user.email.lower(),
        password_hash=CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password_hash)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: userSchemas.UserUpdate):
    db_user = db.query(userModel.User).filter(userModel.User.user_id == user.user_id).first()

    try:
        if user.username is not None:
            db_user.username = user.username
        if user.email is not None:
            db_user.email = user.email.lower()
        if user.password_hash is not None:
            db_user.password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password_hash)

        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_user

def delete_user(db: Session, uid: int):
    db_user = db.query(userModel.User).filter(userModel.User.user_id == uid).first()
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "User deleted"})