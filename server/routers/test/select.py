from fastapi import APIRouter, Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db
from schemas.test import SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, utils
from routers.test import utils as test_utils

from crud.mongo.user import find_users as mongo_find_users
from crud.mongo.device import find_devices as mongo_find_devices
from crud.mongo.device_gesture import find_gestures_by_device_ids as mongo_find_device_gestures

from crud.postgresql.testingCrud import selectUsersTest, selectDevicesTest, selectDeviceGesturesTest

router = APIRouter()


@router.post("/user", response_model=ExecutionTime)
def select_users(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    user_id_map_df = test_utils.get_users_id_map()
    postgres_users_id, mongo_users_id = test_utils.get_random_ids(user_id_map_df, rows_count)
    postgres_users_id = utils.IdListRequest(id_list=postgres_users_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_find_users(mongo_db, mongo_users_id)
        mongo_times.append(mongo_time)
        postgres_time = selectUsersTest(postgres_users_id, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.post("/device", response_model=ExecutionTime)
def select_devices(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    user_id_map_df = test_utils.get_users_id_map()
    postgres_users_id, mongo_users_id = test_utils.get_random_ids(user_id_map_df, rows_count)
    postgres_users_id = utils.IdListRequest(id_list=postgres_users_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_find_devices(mongo_db, mongo_users_id)
        mongo_times.append(mongo_time)
        postgres_time = selectDevicesTest(postgres_users_id, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.post("/device_gestures", response_model=ExecutionTime)
def select_device_gestures(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    device_id_map_df = test_utils.get_devices_id_map()
    postgres_devices_id, mongo_devices_id = test_utils.get_random_ids(device_id_map_df, rows_count)
    postgres_devices_id = utils.IdListRequest(id_list=postgres_devices_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_find_device_gestures(mongo_db, mongo_devices_id)
        mongo_times.append(mongo_time)
        postgres_time = selectDeviceGesturesTest(postgres_devices_id, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)
