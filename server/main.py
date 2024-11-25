from fastapi import FastAPI
from server.routers.postgresql import basicRouter, userRouter, gestureRouter, deviceRouter, deviceGestureRouter, gestureLogsRouter
from server.core.postgresql import database

#load_dotenv()

#JSON_DIR = f'{os.getenv("MONGO_DATA_DIR")}/'
#CSV_DIR = f'{os.getenv("POSTGRES_DATA_DIR")}/'
#os.makedirs(JSON_DIR, exist_ok=True)
#os.makedirs(CSV_DIR, exist_ok=True)

app = FastAPI()

#app.add_event_handler("startup", connect_to_mongo)
#app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(basicRouter.router)

app.include_router(userRouter.router)

app.include_router(gestureRouter.router)

app.include_router(deviceRouter.router)

app.include_router(deviceGestureRouter.router)

app.include_router(gestureLogsRouter.router)

#app.include_router(mongo_user_router.router, prefix="/mongo/users", tags=["users"])
#app.include_router(mongo_device_router.router, prefix="/mongo/devices", tags=["devices"])
#app.include_router(mongo_device_gesture_router.router, prefix="/mongo/device_gestures", tags=["device_gestures"])
#app.include_router(mongo_gesture_log_router.router, prefix="/mongo/gesture_logs", tags=["gesture_logs"])
#app.include_router(import_data_router, tags=["import_data"])

database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)
