from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from routers import basic, user, gesture
import models, schemas, database, crud

app = FastAPI()

app.include_router(basic.router)

app.include_router(user.router)

app.include_router(gesture.router)



database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)