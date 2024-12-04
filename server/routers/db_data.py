from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from server.data_generator import generate_data_and_export
import subprocess
import os
from pymongo.database import Database

from server.schemas.db_data import ImportRequest
from server.core.mongo.database import get_db
from server.core.postgresql.utils import (
    import_users,
    import_device_types,
    import_gestures,
    import_devices,
    import_device_gestures,
    import_gesture_logs,
    clear_database
)
from server.core.postgresql import database

router = APIRouter()


@router.post("/import")
def import_data(request: ImportRequest, db_postgre: Session = Depends(database.get_db)):
    generate_data_and_export(
        user_count=request.user_count,
        device_count_range=request.device_count_range,
        gesture_count_range=request.gesture_count_range,
        log_count=request.log_count
    )

    # Wykonanie mongoimport za pomocą subprocess
    json_files = ["users.json", "devices.json", "gesture_logs.json"]
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "gesture_control")

    for file in json_files:
        file_path = f'../{os.getenv("MONGO_DATA_DIR")}/{file}'
        if os.path.exists(file_path):
            run_mongoimport_in_docker(f'{os.getenv("MONGO_CONTAINER_NAME")}', mongo_uri, db_name, file)

    run_postgre_import(db_postgre)

    return {"message": "Data imported successfully"}


@router.post("/delete")
def delete_data(db: Database = Depends(get_db), db_postgre: Session = Depends(database.get_db)):
    try:
        collections = db.list_collection_names()

        for collection_name in collections:
            if collection_name != "system.profile":
                db[collection_name].delete_many({})

        clear_postgre(db_postgre)

        return {"message": "All data deleted successfully"}

    except Exception as e:
        return {"error": str(e)}


def run_mongoimport_in_docker(mongo_container_name, mongo_uri, db_name, file_path):
    # Wywołanie mongoimport w kontenerze Docker
    mongoimport_command = [
        "docker", "exec", mongo_container_name,
        "mongoimport",
        "--uri", mongo_uri,
        "--db", db_name,
        "--collection", file_path.split('.')[0],
        "--file", f'/{os.getenv("MONGO_DATA_DOCKER_DIR")}/{file_path}',  # Plik JSON w kontenerze
        "--jsonArray",
        "--drop"
    ]

    try:
        subprocess.run(mongoimport_command, check=True)
        print(f"Plik {file_path} zaimportowany pomyślnie!")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas importowania pliku {file_path}: {e}")


def run_postgre_import(db: Session):
    import_users(db)
    import_device_types(db)
    import_gestures(db)
    import_devices(db)
    import_device_gestures(db)
    import_gesture_logs(db)


def clear_postgre(db: Session):
    clear_database(db)