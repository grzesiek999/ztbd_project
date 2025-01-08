
from sqlalchemy import text
from fastapi import HTTPException
from sqlalchemy.orm import Session


def execute_copy(db: Session, table_name: str, file_path: str):
    """Helper function to execute COPY command"""
    try:
        with db.connection().connection.cursor() as cursor:
            copy_command = f"""
            COPY "{table_name}"
            FROM '{file_path}'
            DELIMITER ',' CSV HEADER;
            """
            cursor.execute(copy_command)
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error importing data into {table_name}: {str(e)}")


def import_users(db: Session):
    file_path = "/csv/users.csv"
    execute_copy(db, "users", file_path)
    return {"message": "Users imported successfully"}


def import_device_types(db: Session):
    file_path = "/csv/device_types.csv"
    execute_copy(db, "deviceTypes", file_path)
    return {"message": "Device types imported successfully"}


def import_gestures(db: Session):
    file_path = "/csv/gestures.csv"
    execute_copy(db, "gestures", file_path)
    return {"message": "Gestures imported successfully"}


def import_devices(db: Session):
    file_path = "/csv/devices.csv"
    execute_copy(db, "devices", file_path)
    return {"message": "Devices imported successfully"}


def import_device_gestures(db: Session):
    file_path = "/csv/device_gestures.csv"
    execute_copy(db, "device_gestures", file_path)
    return {"message": "Device gestures imported successfully"}


def import_gesture_logs(db: Session):
    file_path = "/csv/gesture_logs.csv"
    execute_copy(db, "gestureLogs", file_path)
    return {"message": "Gesture logs imported successfully"}


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