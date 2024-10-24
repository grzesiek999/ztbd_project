from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from routers import user
import models, schemas, database

app = FastAPI()

app.include_router(user.router)

database.Base.metadata.create_all(bind=database.engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
@app.get("/")
def read_root():
    return {"message": "Hello World!"}

