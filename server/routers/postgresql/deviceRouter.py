from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.postgresql import deviceSchemas, utils
from crud.postgresql import userCrud, deviceCrud, deviceTypeCrud
from core.postgresql import database
from typing import List
import time



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

    db_device_type = deviceTypeCrud.get_device_type_by_id(db, device.device_type_id)
    if db_device_type is None:
        raise HTTPException(status_code=404, detail="DeviceType not found !")

    return deviceCrud.create_device(db, device=device)


@router.patch("/update_device", response_model=deviceSchemas.Device)
def update_device(device: deviceSchemas.DeviceUpdate, db: Session = Depends(database.get_db)):

    db_device = deviceCrud.get_device_by_id(db, device.device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return deviceCrud.update_device(db, device=device)


@router.delete("/delete_device")
def delete_device(did: int, db: Session = Depends(database.get_db)):

    db_device = deviceCrud.get_device_by_id(db, did)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found !")

    return deviceCrud.delete_device(db, did)


# Queries to test

@router.get("/get_devices_by_user_id_list", response_model=List[deviceSchemas.Device])
def get_devices_by_user_id_list(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    db_devices = deviceCrud.get_devices_by_user_id_list(db, id_list)
    end = time.time()
    query_time = end - start

    if not db_devices:
        raise HTTPException(status_code=404, detail="No devices found for the provided IDs.")

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.post("/create_devices")
def create_devices(device_list: List[deviceSchemas.DeviceCreate], db: Session = Depends(database.get_db)):

    if not device_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for device in device_list:
        try:
            deviceCrud.create_device(db, device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create device: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.patch("/update_devices")
def update_devices(device_list: List[deviceSchemas.DeviceUpdate], db: Session = Depends(database.get_db)):

    if not device_list:
        raise HTTPException(status_code=400, detail="The cannot be empty.")

    start = time.time()
    for device in device_list:
        try:
            deviceCrud.update_device(db, device)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update device: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})


@router.delete("/delete_devices")
def delete_devices(request: utils.IdListRequest, db: Session = Depends(database.get_db)):
    id_list = request.id_list

    if not id_list:
        raise HTTPException(status_code=400, detail="The id_list cannot be empty.")

    start = time.time()
    for did in id_list:
        try:
            deviceCrud.delete_device(db, did)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    end = time.time()
    query_time = end - start

    return JSONResponse(status_code=200, content={"Query Time:": query_time})