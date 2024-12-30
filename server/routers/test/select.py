from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from sqlalchemy.orm import Session

from core.mongo.database import get_db as get_mongo_db
from core.postgresql import database as get_postgresql_db
from schemas.test import SamplesAndRowsCount, ExecutionTime
from schemas.postgresql import userSchemas, utils

from crud.mongo.user import find_users as mongo_find_users

from crud.postgresql.testingCrud import selectUsersTest

router = APIRouter()


@router.post("/user", response_model=ExecutionTime)
def select_users(request: SamplesAndRowsCount, mongo_db: Database = Depends(get_mongo_db),
                 postgresql_db: Session = Depends(get_postgresql_db.get_db)):
    samples_count = request.samples_count
    rows_count = request.rows_count

    # TODO: Implement users id generation
    postgres_users_id = [1, 2, 3]
    mongo_users_id = ["6772ed6401b43c9a4c9d7e15", "6772ed6401b43c9a4c9d7ddb", "6772ed6401b43c9a4c9d7dfd"]

    postgres_users_id = utils.IdListRequest(id_list=postgres_users_id)

    postgres_times = []
    mongo_times = []

    for i in range(samples_count):
        mongo_time = mongo_find_users(mongo_db, mongo_users_id)
        mongo_times.append(mongo_time)
        postgres_time = selectUsersTest(postgres_users_id, postgresql_db)
        postgres_times.append(postgres_time)

    return ExecutionTime(postgres_execution_times=postgres_times, mongo_execution_times=mongo_times)
