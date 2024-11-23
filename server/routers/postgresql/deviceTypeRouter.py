from fastapi import  APIRouter, Depends, HTTPException
from server.schemas.postgresql import deviceTypeSchemas
from server.crud.postgresql import deviceTypeCrud
from sqlalchemy.orm import Session
from server.core import database


router = APIRouter(
    prefix="/deviceType",
    tags=["deviceType"],
)

@router.get("/get_device_type_by_id", response_model=deviceTypeSchemas.DeviceType)
def get_device_type_by_id(dtid: int, db: Session = Depends(database.get_db)):
    db_deviceType = deviceTypeCrud.get_device_type_by_id(db, dtid)

    if db_deviceType is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return db_deviceType

@router.get("/get_device_by_type_name", response_model=deviceTypeSchemas.DeviceType)
def get_device_by_type_name(type_name: str, db: Session = Depends(database.get_db)):
    db_deviceType = deviceTypeCrud.get_device_by_type_name(db, type_name)

    if db_deviceType is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return db_deviceType

@router.post("/create_device_type", response_model=deviceTypeSchemas.DeviceType)
def create_device_type(deviceType: deviceTypeSchemas.DeviceTypeCreate, db: Session = Depends(database.get_db)):
    db_device_type = deviceTypeCrud.get_device_by_type_name(db, deviceType.type_name)

    if db_device_type:
        raise HTTPException(status_code=400, detail="DeviceType already exists")

    return deviceTypeCrud.create_device(db, deviceType)

@router.patch("/update_device_type", response_model=deviceTypeSchemas.DeviceType)
def update_device_type(deviceType: deviceTypeSchemas.DeviceTypeUpdate, db: Session = Depends(database.get_db)):
    db_device_type = deviceTypeCrud.get_device_type_by_id(db, deviceType.device_id)

    if db_device_type is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return deviceTypeCrud.update_device(db, deviceType)

@router.delete("/delete_device_type")
def delete_device_type(didt: int, db: Session = Depends(database.get_db)):
    db_deviceType = deviceTypeCrud.get_device_type_by_id(db, didt)

    if db_deviceType is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return deviceTypeCrud.delete_device(db, didt)