from sqlalchemy.orm import Session
from pymongo.database import Database
from fastapi import APIRouter, Depends
import logging

from core.mongo.database import get_db as get_mongo_db
from core.postgresql.database import get_db as get_postgresql_db
from routers.test.delete import delete_users_func, delete_devices_func
from routers.test.plots.plots import execute_and_plot, count_users, count_devices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/users", response_model=int)
def plot_create_delete_users(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                             postgresql_db: Session = Depends(get_postgresql_db)):
    database_users_rows_count = count_users()

    return execute_and_plot(mongo_db, postgresql_db, database_users_rows_count, delete_users_func, test_samples,
                            "delete_users.png")


@router.get("/devices", response_model=int)
def plot_create_delete_devices(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                               postgresql_db: Session = Depends(get_postgresql_db)):
    database_devices_rows_count = count_devices()

    return execute_and_plot(mongo_db, postgresql_db, database_devices_rows_count, delete_devices_func, test_samples,
                            "delete_devices.png")
