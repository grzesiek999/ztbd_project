from sqlalchemy.orm import Session
from pymongo.database import Database
from fastapi import APIRouter, Depends
import logging

from core.mongo.database import get_db as get_mongo_db
from core.postgresql.database import get_db as get_postgresql_db
from routers.test.insert import insert_users_func, insert_devices_func
from routers.test.plots.plots import execute_and_plot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/users", response_model=int)
def plot_create_insert_users(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                             postgresql_db: Session = Depends(get_postgresql_db)):
    max_users_to_insert = 100000
    return execute_and_plot(mongo_db, postgresql_db, max_users_to_insert, insert_users_func, test_samples,
                            "insert_users.png")


@router.get("/devices", response_model=int)
def plot_create_insert_devices(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                               postgresql_db: Session = Depends(get_postgresql_db)):
    max_devices_to_insert = 100000
    return execute_and_plot(mongo_db, postgresql_db, max_devices_to_insert, insert_devices_func, test_samples,
                            "insert_devices.png")
