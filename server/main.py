from fastapi import FastAPI
from server.routers.postgresql import deviceRouter, basicRouter, userRouter, userGestureRouter, gestureRouter
from server.core import database

app = FastAPI()

app.include_router(basicRouter.router)

app.include_router(userRouter.router)

app.include_router(gestureRouter.router)

app.include_router(deviceRouter.router)

app.include_router(userGestureRouter.router)


database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)