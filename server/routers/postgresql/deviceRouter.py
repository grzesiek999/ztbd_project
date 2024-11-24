from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.schemas.postgresql import deviceSchemas
from server.crud.postgresql import userCrud, deviceCrud, deviceTypeCrud
from server.core import database
from typing import List


router = APIRouter(
    prefix="/device",
    tags=["device"]
)



@router.get("/get_device_by_id", response_model=deviceSchemas.Device)
def get_device_by_id(did: int, db: Session = Depends(database.get_db)):

    db_device = deviceCrud.get_device_by_id(db, did)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_device


@router.get("/get_devices_by_name", response_model=List[deviceSchemas.Device])
def get_devices_by_name(name: str, db: Session = Depends(database.get_db)):

    db_devices = deviceCrud.get_devices_by_name(db, name)
    if db_devices is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_devices


@router.get("/get_devices_by_device_type_id", response_model=List[deviceSchemas.Device])
def get_devices_by_device_type_id(dtid: int, db: Session = Depends(database.get_db)):

    db_devices = deviceCrud.get_devices_by_device_type_id(db, dtid)
    if db_devices is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return db_devices


@router.post("/create_device", response_model=deviceSchemas.Device)
def create_device(device: deviceSchemas.DeviceCreate, db: Session = Depends(database.get_db)):

    db_user = userCrud.get_user_by_id(db, device.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found !")

    db_device_type_id = deviceTypeCrud.get_device_type_by_id(db, device.device_type_id)
    if db_device_type_id is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return deviceCrud.create_device(db, device=device)


@router.patch("/update_device", response_model=deviceSchemas.Device)
def update_device(device: deviceSchemas.DeviceUpdate, db: Session = Depends(database.get_db)):

    db_device = deviceCrud.get_device_by_id(db, device.id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return deviceCrud.update_device(db, device=device)


@router.delete("/delete_device")
def delete_device(did: int, db: Session = Depends(database.get_db)):

    db_device = deviceCrud.get_device_by_id(db, did)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return deviceCrud.delete_device(db, did)