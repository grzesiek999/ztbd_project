from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import models, schemas
from datetime import datetime


# User CRUD

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.user_email == email).first()

def get_users_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.user_name == name).all()

def get_users_by_created_at(db: Session, created_at: datetime):
    target_date = created_at.date()
    return db.query(models.User).filter(func.date(models.User.created_at) == target_date).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        user_name=user.user_name,
        user_email=user.user_email.lower(),
        password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def path_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.user_email == user.user_email).first()

    if db_user is None:
        return False

    try:
        if user.user_name:
            db_user.user_name = user.user_name
        if user.user_email:
            db_user.user_email = user.user_email.lower()
        if user.password:
            db_user.password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(user.pasword)

        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_user


# Gesture CRUD
