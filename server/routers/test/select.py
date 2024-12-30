import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from sqlalchemy.orm import Session
import pandas as pd

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db
from schemas.test import SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, utils
from routers.test import utils as test_utils

from crud.mongo.user import find_users as mongo_find_users

from crud.postgresql.testingCrud import selectUsersTest

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
