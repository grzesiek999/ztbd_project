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
from routers.test import select as test_select_router
from routers.test import insert as test_insert_router
from routers.test import update as test_update_router
from routers.test import delete as test_delete_router
from routers.test.plots.select import router as plot_router_select
from routers.test.plots.insert import router as plot_router_insert
from routers.test.plots.update import router as plot_router_update
from routers.test.plots.delete import router as plot_router_delete
from routers.test.plots.no_rows_gestures import router as plot_router_gestures
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


app.include_router(plot_router_select, prefix="/plot/select", tags=["Plot select"])
app.include_router(plot_router_insert, prefix="/plot/insert", tags=["Plot insert"])
app.include_router(plot_router_update, prefix="/plot/update", tags=["Plot update"])
app.include_router(plot_router_delete, prefix="/plot/delete", tags=["Plot delete"])
app.include_router(plot_router_gestures, prefix="/plot/gestures", tags=["Plot/CSV gestures"])

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

app.include_router(test_select_router.router, prefix="/test/select", tags=["Test SELECT"])
app.include_router(test_insert_router.router, prefix="/test/insert", tags=["Test INSERT"])
app.include_router(test_update_router.router, prefix="/test/update", tags=["Test UPDATE"])
app.include_router(test_delete_router.router, prefix="/test/delete", tags=["Test DELETE"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=reload)
