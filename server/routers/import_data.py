from fastapi import APIRouter, HTTPException
from server.data_generator import generate_data_and_export
import subprocess
import os

from server.schemas.mongo.import_data import ImportRequest

router = APIRouter()


@router.post("/import")
def import_data(request: ImportRequest):
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
        file_path = f"../{os.getenv("MONGO_DATA_DIR")}/{file}"
        if os.path.exists(file_path):
            run_mongoimport_in_docker(f"{os.getenv("MONGO_CONTAINER_NAME")}", mongo_uri, db_name, file)

    # TODO: Import CSV files to Postgres

    return {"message": "Data imported successfully"}


def run_mongoimport_in_docker(mongo_container_name, mongo_uri, db_name, file_path):
    # Wywołanie mongoimport w kontenerze Docker
    mongoimport_command = [
        "docker", "exec", mongo_container_name,
        "mongoimport",
        "--uri", mongo_uri,
        "--db", db_name,
        "--collection", file_path.split('.')[0],
        "--file", f"/{os.getenv("MONGO_DATA_DOCKER_DIR")}/{file_path}",  # Plik JSON w kontenerze
        "--jsonArray",
        "--drop"
    ]

    try:
        subprocess.run(mongoimport_command, check=True)
        print(f"Plik {file_path} zaimportowany pomyślnie!")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas importowania pliku {file_path}: {e}")
