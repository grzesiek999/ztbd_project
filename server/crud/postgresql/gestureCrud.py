from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import gestureModel
from server.schemas.postgresql import gestureSchemas



# Gesture CRUD

def get_gesture_by_id(db: Session, gid: int):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.id == gid).first()

def get_gesture_by_type(db: Session, type: str):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_type == type).first()

def create_gesture(db: Session, gesture: gestureSchemas.GestureCreate):
    db_gesture = gesture.Gesture(
        gesture_name=gesture.gesture_name.lower(),
        gesture_description=gesture.gesture_description.lower()
    )

    db.add(db_gesture)
    db.commit()
    db.refresh(db_gesture)
    return db_gesture

def update_gesture(db: Session, gesture: gestureSchemas.GestureUpdate):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.id == gesture.id).first()

    try:
        if gesture.gesture_name is not None:
            db_gesture.gesture_name = gesture.gesture_name.lower()
        if gesture.gesture_description is not None:
            db_gesture.gesture_description = gesture.gesture_description.lower()

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture

def delete_gesture(db: Session, gid: int):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.id == gid).first()
    db.delete(db_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Gesture deleted"})