from fastapi import APIRouter, Depends
from pymongo.database import Database
from sqlalchemy.orm import Session

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db

from schemas.test import SamplesCount, SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, deviceSchemas, deviceGestureSchemas
from models.postgresql import userModel
from schemas.mongo.user import UserCreate as MongoUserCreate
from schemas.mongo.device import DeviceCreate as MongoDeviceCreate
from schemas.mongo.device_gesture import DeviceGestureCreate, BulkDeviceGesturesCreate

from routers.test import utils as test_utils
from data_generator import generate_user, generate_device, generate_device_gesture, generate_device_type
from routers.db_data import drop_and_import_data

from crud.mongo.user import insert_users as mongo_insert_users
from crud.mongo.device import insert_devices as mongo_insert_devices
from crud.mongo.device_gesture import insert_gestures_by_device_type as mongo_insert_device_gestures
from crud.postgresql.testingCrud import insertUsersTest, insertDevicesTest, insertDeviceGesturesTest

router = APIRouter()


@router.post("/user", response_model=ExecutionTime)
def insert_users(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    return insert_users_func(request, mongo_db, postgresql_db)


def insert_users_func(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                      postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    mongo_users = []
    postgres_users = []
    for i in range(rows_count):
        user = generate_user()
        user.pop('id', None)
        user.pop('created_at', None)
        mongo_users.append(MongoUserCreate(**user))
        postgres_users.append(userSchemas.UserCreate(**user))

    postgres_times = []
    mongo_times = []

    # Wake up the database
    v = mongo_db.users.find({}).limit(1)
    v2 = postgresql_db.query(userModel.User).limit(1)
    for i in range(samples_count):
        drop_and_import_data(postgresql_db)

        mongo_time = mongo_insert_users(mongo_db, mongo_users)
        mongo_times.append(mongo_time)
        postgres_time = insertUsersTest(postgres_users, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.post("/device", response_model=ExecutionTime)
def insert_devices(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                   postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    return insert_devices_func(request, mongo_db, postgresql_db)


def insert_devices_func(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                        postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count
    user_id_map_df = test_utils.get_users_id_map()

    mongo_devices = []
    postgres_devices = []
    for i in range(rows_count):
        random_idx_user = user_id_map_df.sample(n=1)
        postgre_user_id = random_idx_user.iloc[0]['postgres_id']
        mongo_user_id = random_idx_user.iloc[0]['mongo_id']

        device = generate_device(mongo_user_id)
        device.pop('id', None)
        device_type_id = device.pop('device_type_id', None)
        device_mongo = device.copy()
        mongo_devices.append(MongoDeviceCreate(**device_mongo))

        device.pop('owner_id', None)
        device['user_id'] = postgre_user_id
        device['device_type_id'] = device_type_id
        postgres_devices.append(deviceSchemas.DeviceCreate(**device))

    postgres_times = []
    mongo_times = []

    # Wake up the database
    v = mongo_db.users.find({}).limit(1)
    v2 = postgresql_db.query(userModel.User).limit(1)
    for i in range(samples_count):
        drop_and_import_data(postgresql_db)

        mongo_time = mongo_insert_devices(mongo_db, mongo_devices)
        mongo_times.append(mongo_time)
        postgres_time = insertDevicesTest(postgres_devices, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)


@router.post("/gesture", response_model=ExecutionTime)
def insert_gestures(request: SamplesCount, mongo_db: Database = Depends(get_mongo_db),
                    postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    return insert_gestures_func(request, mongo_db, postgresql_db)


def insert_gestures_func(request: SamplesCount, mongo_db: Database = Depends(get_mongo_db),
                         postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count

    device_type = generate_device_type()
    gesture = generate_device_gesture()
    gesture["gesture_description"] = gesture.pop("description", None)
    gesture_id = gesture.pop('id', None)

    mongo_gesture_and_devicetype = BulkDeviceGesturesCreate(device_type=device_type,
                                                            gesture=DeviceGestureCreate(**gesture))
    postgres_gesture_and_devicetype = deviceGestureSchemas.DeviceGestureCreateTest(device_type_name=device_type,
                                                                                   gesture_name=gesture["gesture_name"],
                                                                                   gesture_id=gesture_id)

    postgres_times = []
    mongo_times = []

    # Wake up the database
    v = mongo_db.users.find({}).limit(1)
    v2 = postgresql_db.query(userModel.User).limit(1)
    for i in range(samples_count):
        drop_and_import_data(postgresql_db)

        mongo_time = mongo_insert_device_gestures(mongo_db, mongo_gesture_and_devicetype)
        mongo_times.append(mongo_time)
        postgres_time = insertDeviceGesturesTest(postgres_gesture_and_devicetype, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)
