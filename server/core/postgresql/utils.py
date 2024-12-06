from fastapi import HTTPException
from sqlalchemy.orm import Session
import os
import csv
from models.postgresql.userModel import User
from models.postgresql.gestureModel import Gesture
from models.postgresql.deviceTypeModel import DeviceType
from models.postgresql.deviceModel import Device
from models.postgresql.deviceGestureModel import DeviceGesture
from models.postgresql.gestureLogsModel import GestureLogs
from datetime import datetime
from sqlalchemy import text




def import_users(db: Session):
    file_path = os.path.join("data", "csv", "users.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                existing_user = db.query(User).filter(User.email == row["email"]).first()
                if existing_user:
                    print(f"User with email {row['email']} already exists. Skipping...")
                    skipped_count += 1
                    continue

                try:
                    user = User(
                        user_id=int(row["user_id"]),
                        username=row["username"],
                        email=row["email"],
                        password_hash=row["password_hash"],
                        created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
                    )
                    db.add(user)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add user with email {row['email']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "User import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing users: {str(e)}")



def import_device_types(db: Session):
    file_path = os.path.join("data", "csv", "device_types.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                existing_device_type = db.query(DeviceType).filter(DeviceType.type_name == row["type_name"]).first()
                if existing_device_type:
                    print(f"Device Type with type_name {row['type_name']} already exists. Skipping...")
                    skipped_count += 1
                    continue

                try:
                    device_type = DeviceType(
                        device_type_id=int(row["device_type_id"]),
                        type_name=row["type_name"],
                    )
                    db.add(device_type)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add device_type with type_name {row['type_name']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "DeviceType import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing deviceTypes: {str(e)}")



def import_gestures(db: Session):
    file_path = os.path.join("data", "csv", "gestures.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                existing_gesture = db.query(Gesture).filter(Gesture.gesture_type == row["gesture_type"]).first()
                if existing_gesture:
                    print(f"Gesture with type {row['gesture_type']} already exists. Skipping...")
                    skipped_count += 1
                    continue

                try:
                    gesture = Gesture(
                        gesture_id=int(row["gesture_id"]),
                        gesture_type=row["gesture_type"],
                        description=row["description"],
                    )
                    db.add(gesture)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add gesture with gesture_type {row['gesture_type']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "Gesture import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing gestures: {str(e)}")



def import_devices(db: Session):
    file_path = os.path.join("data", "csv", "devices.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                try:
                    device = Device(
                        device_id=int(row["device_id"]),
                        device_type_id=row["device_type_id"],
                        device_name=row["device_name"],
                        user_id=row["user_id"],
                    )
                    db.add(device)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add device with id {row['device_id']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "Device import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing devices: {str(e)}")



def import_device_gestures(db: Session):
    file_path = os.path.join("data", "csv", "device_gestures.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                try:
                    device_gestures = DeviceGesture(
                        device_gesture_id=int(row["device_gesture_id"]),
                        gesture_id=row["gesture_id"],
                        gesture_name=row["gesture_name"],
                        device_id=row["device_id"],
                    )
                    db.add(device_gestures)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add device_gesture with id {row['device_gesture_id']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "DeviceGesture import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing device gestures: {str(e)}")



def import_gesture_logs(db: Session):
    file_path = os.path.join("data", "csv", "gesture_logs.csv")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File {file_path} not found.")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)

            imported_count = 0
            skipped_count = 0

            for row in csv_reader:
                try:
                    gesture_logs = GestureLogs(
                        log_id=int(row["log_id"]),
                        device_gesture_id=row["device_gesture_id"],
                        timestamp=row["timestamp"],
                    )
                    db.add(gesture_logs)
                    db.commit()
                    imported_count += 1
                except Exception as e:
                    db.rollback()
                    print(f"Failed to add gesture_logs with id {row['log_id']}: {str(e)}")
                    skipped_count += 1

            return {
                "message": "Gesture Logs import completed.",
                "imported_count": imported_count,
                "skipped_count": skipped_count,
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing gesture logs: {str(e)}")



def clear_database(db: Session):
    try:
        db.execute(text("SET session_replication_role = 'replica';"))
        db.commit()

        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """))
        tables = [row[0] for row in result]

        for table in tables:
            db.execute(text(f'TRUNCATE TABLE "{table}" CASCADE;'))

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Błąd podczas czyszczenia bazy danych: {str(e)}")
    finally:
        db.execute(text("SET session_replication_role = 'origin';"))
        db.commit()