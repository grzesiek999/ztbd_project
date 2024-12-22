import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# import debugpy

from routers.postgresql import basicRouter, userRouter, gestureRouter, deviceRouter, deviceGestureRouter, gestureLogsRouter
from routers.db_data import router as import_data_router
from routers.mongo import user as mongo_user_router
from routers.mongo import device as mongo_device_router
from routers.mongo import device_gesture as mongo_device_gesture_router
from routers.mongo import log as mongo_gesture_log_router
from core.mongo.database import connect_to_mongo, close_mongo_connection
from core.postgresql.database import connect_to_postgres, close_postgres_connection

load_dotenv()

environment = os.getenv("ENVIRONMENT", "prod")

if environment == "dev":
    # debugpy.listen(('0.0.0.0', 5678))
    # print("Czekam na połączenie debugera...")
    # debugpy.wait_for_client()
    # print("Debuger polaczony")
    reload = True
else:
    reload = False

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_event_handler("startup", connect_to_postgres)
app.add_event_handler("shutdown", close_postgres_connection)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
