from typing import List
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from server.schemas.mongo.user import UserOut, UserCreate, UserUpdate
from server.crud.mongo import user as crud_user
from server.core.mongo.database import get_db

router = APIRouter()


@router.get("/", response_model=List[UserOut])
async def read_users(db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_user.get_users(db)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await crud_user.create_user(db, user_in)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user_in: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud_user.update_user(db, user_id, user_in)


@router.delete("/{user_id}")
async def delete_user(user_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    user = await crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await crud_user.delete_user(db, user_id)
    return {"detail": "User deleted"}
