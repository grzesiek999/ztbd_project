from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.postgresql import gestureModel
from schemas.postgresql import gestureSchemas



# Gesture CRUD

def get_gesture_by_id(db: Session, gid: int):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_id == gid).first()

def get_gesture_by_type(db: Session, type: str):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_type == type).first()

def create_gesture(db: Session, gesture: gestureSchemas.GestureCreate):
    db_gesture = gesture.Gesture(
        gesture_type=gesture.gesture_type.lower(),
        description=gesture.description.lower()
    )

    db.add(db_gesture)
    db.commit()
    db.refresh(db_gesture)
    return db_gesture

def update_gesture(db: Session, gesture: gestureSchemas.GestureUpdate):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_id == gesture.gesture_id).first()

    try:
        if gesture.gesture_type is not None:
            db_gesture.gesture_type = gesture.gesture_type.lower()
        if gesture.description is not None:
            db_gesture.description = gesture.description.lower()

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture

def delete_gesture(db: Session, gid: int):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_id == gid).first()
    db.delete(db_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Gesture deleted"})

def update_gesture_by_type(db: Session, gesture: gestureSchemas.GestureUpdateByType):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_type == gesture.gesture_type).first()

    try:
        if gesture.description is not None:
            db_gesture.description = gesture.description

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture