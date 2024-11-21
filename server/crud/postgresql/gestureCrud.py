from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import gestureModel
from server.schemas.postgresql import gestureSchemas



# Gesture CRUD

def get_gesture_by_id(db: Session, gesture_id: int):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.id == gesture_id).first()

def get_gestures_by_name(db: Session, gesture_name: str):
    return db.query(gestureModel.Gesture).filter(gestureModel.Gesture.gesture_name == gesture_name).all()

def create_gesture(db: Session, gesture: gestureSchemas.GestureCreate):
    db_gesture = gesture.Gesture(
        gesture_name=gesture.gesture_name.lower(),
        description=gesture.description.lower()
    )

    db.add(db_gesture)
    db.commit()
    db.refresh(db_gesture)
    return db_gesture

def update_gesture(db: Session, gesture: gestureSchemas.GestureUpdate):
    db_gesture = db.query(gesture.Gesture).filter(gesture.Gesture.id == gesture.id).first()

    try:
        if gesture.gesture_name is not None:
            db_gesture.gesture_name = gesture.gesture_name.lower()
        if gesture.description is not None:
            db_gesture.description = gesture.description.lower()

        db.commit()
        db.refresh(db_gesture)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_gesture

def delete_gesture(db: Session, gesture_id: int):
    db_gesture = db.query(gestureModel.Gesture).filter(gestureModel.Gesture.id == gesture_id).first()
    db.delete(db_gesture)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Gesture deleted"})