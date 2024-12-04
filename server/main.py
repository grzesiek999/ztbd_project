import os

from fastapi import FastAPI
from dotenv import load_dotenv

from server.routers.postgresql import basicRouter, userRouter, gestureRouter, deviceRouter, deviceGestureRouter, gestureLogsRouter
from server.core.postgresql import database
from server.routers.db_data import router as import_data_router
from server.routers.mongo import user as mongo_user_router
from server.routers.mongo import device as mongo_device_router
from server.routers.mongo import device_gesture as mongo_device_gesture_router
from server.routers.mongo import log as mongo_gesture_log_router
from server.core.mongo.database import connect_to_mongo, close_mongo_connection

load_dotenv("../.env")

username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
host = os.getenv('MONGO_HOST')
port = os.getenv('MONGO_PORT')
db_name = os.getenv('MONGO_DB_NAME')

mongo_uri = f"mongodb://root:password@localhost:27017/gesture_control?authSource=admin"
os.environ['MONGO_URI'] = mongo_uri

JSON_DIR = f'../{os.getenv("MONGO_DATA_DIR")}/'
CSV_DIR = f'../{os.getenv("POSTGRES_DATA_DIR")}/'
os.makedirs(JSON_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)

app = FastAPI()

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(basicRouter.router)

app.include_router(userRouter.router)

app.include_router(gestureRouter.router)

app.include_router(deviceRouter.router)

app.include_router(deviceGestureRouter.router)

app.include_router(gestureLogsRouter.router)

app.include_router(mongo_user_router.router, prefix="/mongo/users", tags=["Mongo users"])
app.include_router(mongo_device_router.router, prefix="/mongo/devices", tags=["Mongo devices"])
app.include_router(mongo_device_gesture_router.router, prefix="/mongo/device_gestures", tags=["Mongo device_gestures"])
app.include_router(mongo_gesture_log_router.router, prefix="/mongo/gesture_logs", tags=["Mongo gesture_logs"])
app.include_router(import_data_router, prefix="/db", tags=["import_data"])

database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
