from fastapi import APIRouter, Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db

from schemas.test import SamplesCount, SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, deviceSchemas, gestureSchemas
from schemas.mongo.user import UserUpdate as MongoUserUpdate
from schemas.mongo.device import DeviceUpdate as MongoDeviceUpdate
from schemas.mongo.device_gesture import DeviceGestureUpdate

from routers.test import utils as test_utils
from data_generator import generate_user, generate_device, generate_gesture
from routers.db_data import drop_and_import_data

from crud.mongo.user import update_users as mongo_update_users
from crud.mongo.device import update_devices as mongo_update_devices
from crud.mongo.device_gesture import update_gestures_by_type as mongo_update_gestures
from crud.postgresql.testingCrud import updateUsersTest, updateDevicesTest, updateGestureTest

router = APIRouter()


@router.put("/user", response_model=ExecutionTime)
def update_users(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    user_id_map_df = test_utils.get_users_id_map()
    postgres_users_id, mongo_users_id = test_utils.get_random_ids(user_id_map_df, rows_count)

    mongo_users = []
    postgres_users = []
    for i in range(rows_count):
        user = generate_user()
        user.pop('created_at', None)

        # user_mongo = user.copy()
        user['_id'] = mongo_users_id[i]
        mongo_users.append(MongoUserUpdate(**user))

        user.pop('_id', None)
        user['user_id'] = postgres_users_id[i]
        postgres_users.append(userSchemas.UserUpdate(**user))

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_update_users(mongo_db, mongo_users)
        mongo_times.append(mongo_time)
        postgres_time = updateUsersTest(postgres_users, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.put("/device", response_model=ExecutionTime)
def update_devices(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                   postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    device_id_map_df = test_utils.get_devices_id_map()
    postgres_devices_id, mongo_devices_id = test_utils.get_random_ids(device_id_map_df, rows_count)
    user_id_map_df = test_utils.get_users_id_map()

    mongo_devices = []
    postgres_devices = []
    for i in range(rows_count):
        random_idx_user = user_id_map_df.sample(n=1)
        postgre_user_id = random_idx_user.iloc[0]['postgres_id']
        mongo_user_id = random_idx_user.iloc[0]['mongo_id']

        device = generate_device(mongo_user_id)
        device['_id'] = mongo_devices_id[i]
        device_type_id = device.pop('device_type_id', None)
        # mongo_device = device.copy()
        mongo_devices.append(MongoDeviceUpdate(**device))

        device.pop('_id', None)
        device['device_id'] = postgres_devices_id[i]
        device.pop('owner_id', None)
        device['user_id'] = postgre_user_id
        device['device_type_id'] = device_type_id
        postgres_devices.append(deviceSchemas.DeviceUpdate(**device))

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_update_devices(mongo_db, mongo_devices)
        mongo_times.append(mongo_time)
        postgres_time = updateDevicesTest(postgres_devices, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.put("/gesture", response_model=ExecutionTime)
def update_gestures(request: SamplesCount, mongo_db: Database = Depends(get_mongo_db),
                    postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count

    gesture = generate_gesture()
    gesture.pop('id', None)
    postgres_gesture_cp = gesture.copy()
    postgres_gesture = gestureSchemas.GestureUpdateByType(**postgres_gesture_cp)
    gesture['gesture_description'] = gesture.pop('description')
    mongo_gesture = DeviceGestureUpdate(**gesture)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_update_gestures(mongo_db, mongo_gesture)
        mongo_times.append(mongo_time)
        postgres_time = updateGestureTest(postgres_gesture, postgresql_db)
        postgres_times.append(postgres_time)

        drop_and_import_data(postgresql_db)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)
