from sqlalchemy.orm import Session
from pymongo.database import Database
from fastapi import APIRouter, Depends
import logging

from core.mongo.database import get_db as get_mongo_db
from core.postgresql.database import get_db as get_postgresql_db
from routers.test.plots.plots import perform_tests_database_set, plot_create_gestures_separate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# csv_files = {
#     "smallDB_insert_gestures.csv": "/data/smallDB_insert_gestures.csv",
#     "smallDB_update_gestures.csv": "/data/smallDB_update_gestures.csv",
#     "smallDB_delete_gestures.csv": "/data/smallDB_delete_gestures.csv",
#     "mediumDB_insert_gestures.csv": "/data/mediumDB_insert_gestures.csv",
#     "mediumDB_update_gestures.csv": "/data/mediumDB_update_gestures.csv",
#     "mediumDB_delete_gestures.csv": "/data/mediumDB_delete_gestures.csv",
#     "largeDB_insert_gestures.csv": "/data/largeDB_insert_gestures.csv",
#     "largeDB_update_gestures.csv": "/data/largeDB_update_gestures.csv",
#     "largeDB_delete_gestures.csv": "/data/largeDB_delete_gestures.csv",
# }

files = {
    "insert": {
        "small": "/data/smallDB_insert_gestures.csv",
        "medium": "/data/mediumDB_insert_gestures.csv",
        "large": "/data/largeDB_insert_gestures.csv"
    },
    "update": {
        "small": "/data/smallDB_update_gestures.csv",
        "medium": "/data/mediumDB_update_gestures.csv",
        "large": "/data/largeDB_update_gestures.csv"
    },
    "delete": {
        "small": "/data/smallDB_delete_gestures.csv",
        "medium": "/data/mediumDB_delete_gestures.csv",
        "large": "/data/largeDB_delete_gestures.csv"
    }
}


@router.get("/smallDB", response_model=int)
def plot_create_gestures_smallDB(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                                 postgresql_db: Session = Depends(get_postgresql_db)):
    return perform_tests_database_set(mongo_db, postgresql_db, db_size="small", test_samples=test_samples)


@router.get("/mediumDB", response_model=int)
def plot_create_gestures_mediumDB(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                                  postgresql_db: Session = Depends(get_postgresql_db)):
    return perform_tests_database_set(mongo_db, postgresql_db, db_size="medium", test_samples=test_samples)


@router.get("/largeDB", response_model=int)
def plot_create_gestures_largeDB(test_samples: int = 10, mongo_db: Database = Depends(get_mongo_db),
                                 postgresql_db: Session = Depends(get_postgresql_db)):
    return perform_tests_database_set(mongo_db, postgresql_db, db_size="large", test_samples=test_samples)


@router.get("/plot")
def plot_create_gestures_plot():
    plot_create_gestures_separate(files, "/data")
