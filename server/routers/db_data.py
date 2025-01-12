from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data_generator import generate_data_and_export
import subprocess
import os
import time
import logging
from pymongo.database import Database

from schemas.db_data import ImportRequest
from core.mongo.database import get_db
from core.postgresql.utils import (
    import_users,
    import_device_types,
    import_gestures,
    import_devices,
    import_device_gestures,
    import_gesture_logs,
    clear_database
)
from core.postgresql import database
import paramiko
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/import")
def import_data(request: ImportRequest, db_postgre: Session = Depends(database.get_db)):
    """ Generate data and import it into the databases """
    generate_data_and_export(
        user_count=request.user_count,
        device_count_range=request.device_count_range,
        gesture_count_range=request.gesture_count_range,
        log_count=request.log_count
    )

    return drop_and_import_data(db_postgre)


def drop_and_import_data(db_postgre: Session = Depends(database.get_db)):
    """ Drop all data from the databases and import the generated data """
    start_time_mongo_import = time.time()
    mongo_import()
    end_time_mongo_import = time.time()
    mongo_import_time = end_time_mongo_import - start_time_mongo_import
    logger.info(f"Czas wykonania mongo import: {mongo_import_time:.2f} sekund")

    start_time_postgre_delete = time.time()
    delete_data(db_postgre)
    end_time_postgre_delete = time.time()
    postgre_delete_time = end_time_postgre_delete - start_time_postgre_delete
    logger.info(f"Czas wykonania postgre delete: {postgre_delete_time:.2f} sekund")

    start_time_postgre_import = time.time()
    run_postgre_import(db_postgre)
    end_time_postgre_import = time.time()
    postgre_import_time = end_time_postgre_import - start_time_postgre_import
    logger.info(f"Czas wykonania postgre import: {postgre_import_time:.2f} sekund")

    return {"message": "Data imported successfully"}


# @router.post("/delete")
def delete_data(db_postgre: Session = Depends(database.get_db)):
    try:
        clear_postgre(db_postgre)
        return {"message": "All data deleted successfully"}

    except Exception as e:
        return {"error": str(e)}


def mongo_import() -> None:
    json_files = ["users.json", "devices.json", "gesture_logs.json"]
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "gesture_control")
    mongo_data_dir = os.getenv("MONGO_DATA_DOCKER_DIR", "json")

    username = os.getenv("MONGO_SSH_USERNAME")
    password = os.getenv("MONGO_SSH_PASSWORD")
    host_name = os.getenv("MONGO_CONTAINER_NAME")

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host_name, port=22, username=username, password=password)

    for file in json_files:
        file_path = f'/{mongo_data_dir}/{file}'
        run_mongoimport_file(
            mongo_uri=mongo_uri,
            db_name=db_name,
            file_path=file_path,
            ssh_client=ssh_client
        )
    ssh_client.close()


def run_mongoimport_file(mongo_uri: str, db_name: str, file_path: str, ssh_client) -> None:
    collection_name = file_path.split('/')[-1].split('.')[0]

    command = f"mongoimport --uri {mongo_uri} --db {db_name} --collection {collection_name} --file {file_path} --jsonArray --drop"
    stdin, stdout, stderr = ssh_client.exec_command(command)

    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    if output:
        print(output)
    if error:
        print(f"Error importing data into {db_name}.{collection_name}, error: {error}")
    else:
        print(f"Data imported successfully into {db_name}.{collection_name}")


def run_postgre_import(db: Session):
    import_users(db)
    import_device_types(db)
    import_gestures(db)
    import_devices(db)
    import_device_gestures(db)


def clear_postgre(db: Session):
    clear_database(db)
