from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext
import models, schemas
from datetime import datetime


# User CRUD

def get_user_by_id(db: Session, user_id: int):
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

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()

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


# Gesture CRUD

def get_gesture_by_id(db: Session, gesture_id: int):
    return db.query(models.Gesture).filter(models.Gesture.id == gesture_id).first()

def get_gesture_by_name(db: Session, gesture_name: str):
    return db.query(models.Gesture).filter(models.Gesture.gesture_name == gesture_name).first()

def create_gesture(db: Session, gesture: schemas.GestureCreate):
    db_gesture = models.Gesture(
        gesture_name=gesture.gesture_name.lower(),
        description=gesture.description.lower()
    )

    db.add(db_gesture)
    db.commit()
    db.refresh(db_gesture)
    return db_gesture

def update_gesture(db: Session, gesture: schemas.GestureUpdate):
    db_gesture = db.query(models.Gesture).filter(models.Gesture.id == gesture.id).first()

    try:
        if db_gesture.gesture_name is not None:
            db_gesture.gesture_name = gesture.gesture_name.lower()
        if db_gesture.description is not None:
            db_gesture.description = gesture.description.lower()

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture


# Device CRUD