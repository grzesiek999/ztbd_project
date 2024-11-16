from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server import crud, database
from server.schemas.posrgresql import schemas
from typing import List


router = APIRouter(
    prefix="/device",
    tags=["device"]
)

@router.get("/get_device_by_id", response_model=schemas.Device)
def get_device_by_id(did: int, db: Session = Depends(database.get_db)):
    db_device = crud.get_device_by_id(db, device_id=did)

    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_device

@router.get("/get_devices_by_name", response_model=List[schemas.Device])
def get_devices_by_name(name: str, db: Session = Depends(database.get_db)):
    db_devices = crud.get_devices_by_name(db, device_name=name)

    if db_devices is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_devices

@router.get("/get_devices_by_type", response_model=List[schemas.Device])
def get_devices_by_type(dtype: str, db: Session = Depends(database.get_db)):
    db_devices = crud.get_devices_by_type(db, device_type=dtype)

    if db_devices is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_devices

@router.post("/create_device", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_id(db, user_id=device.user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    return crud.create_device(db, device=device)

@router.patch("/update_device", response_model=schemas.Device)
def update_device(device: schemas.DeviceUpdate, db: Session = Depends(database.get_db)):
    db_device = crud.get_device_by_id(db, device_id=device.id)

    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return crud.update_device(db, device=device)

@router.delete("/delete_device")
def delete_device(did: int, db: Session = Depends(database.get_db)):
    db_device = crud.get_device_by_id(db, device_id=did)

    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return crud.delete_device(db, device_id=did)