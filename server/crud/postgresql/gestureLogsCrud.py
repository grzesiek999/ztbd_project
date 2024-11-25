from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import gestureLogsModel



# User CRUD

def get_gesture_log_by_id(db: Session, glid: int):
    return db.query(gestureLogsModel.GestureLogs).filter(gestureLogsModel.GestureLogs.id == glid).first()

