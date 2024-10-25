from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["basic"]
)

@router.get("/")
def read_root():
    return {"message": "Hello World!"}
