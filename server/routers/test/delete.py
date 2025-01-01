from fastapi import APIRouter, Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db

from schemas.test import SamplesCount, SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, deviceSchemas, gestureSchemas, utils
from schemas.mongo.device_gesture import DeviceGestureDeletePattern

from routers.test import utils as test_utils
from data_generator import generate_user, generate_device, generate_device_gesture, generate_device_type, \
    generate_gesture
from routers.db_data import drop_and_import_data

from crud.mongo.user import delete_users as mongo_delete_users
from crud.mongo.device import delete_devices as mongo_delete_devices
from crud.mongo.device_gesture import delete_gestures_by_type as mongo_delete_gestures
from crud.postgresql.testingCrud import deleteUsersTest, deleteDevicesTest, deleteDeviceGesturesTest

router = APIRouter()


@router.delete("/user", response_model=ExecutionTime)
def delete_users(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    user_id_map_df = test_utils.get_users_id_map()
    postgres_users_id, mongo_users_id = test_utils.get_random_ids(user_id_map_df, rows_count)
    postgres_users_id = utils.IdListRequest(id_list=postgres_users_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_delete_users(mongo_db, mongo_users_id)
        mongo_times.append(mongo_time)
        postgres_time = deleteUsersTest(postgres_users_id, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.delete("/device", response_model=ExecutionTime)
def delete_devices(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    device_id_map_df = test_utils.get_devices_id_map()
    postgres_devices_id, mongo_devices_id = test_utils.get_random_ids(device_id_map_df, rows_count)
    postgres_devices_id = utils.IdListRequest(id_list=postgres_devices_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_delete_devices(mongo_db, mongo_devices_id)
        mongo_times.append(mongo_time)
        postgres_time = deleteDevicesTest(postgres_devices_id, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.delete("/gesture", response_model=ExecutionTime)
def delete_gestures(request: SamplesCount, mongo_db: Database = Depends(get_mongo_db),
                    postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count

    gesture = generate_gesture()
    gesture.pop('id', None)
    gesture.pop('description', None)
    postgres_gesture = gesture['gesture_type']
    mongo_gesture = DeviceGestureDeletePattern(**gesture)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_delete_gestures(mongo_db, mongo_gesture)
        mongo_times.append(mongo_time)
        postgres_time = deleteDeviceGesturesTest(postgres_gesture, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


