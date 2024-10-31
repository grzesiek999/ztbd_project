from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server import crud, models, schemas, database
from typing import List


router = APIRouter(
    prefix="/usergesture",
    tags=["UserGesture"]
)