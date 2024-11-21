from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import deviceTypeModel
from server.schemas.postgresql import deviceTypeSchemas


# DeviceType CRUD

def get_device_type_by_id(db: Session, device_type_id: int):
    return db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.id == device_type_id).first()

def get_device_by_type_name(db: Session, device_type_name: str):
    return db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.type_name == device_type_name).all()

def create_device(db: Session, deviceType: deviceTypeSchemas.DeviceTypeCreate):
    db_deviceType = deviceType.Device(
        type_name =  deviceType.type_name.lower(),
    )

    db.add(db_deviceType)
    db.commit()
    db.refresh(db_deviceType)
    return db_deviceType

def update_device(db: Session, deviceType: deviceTypeSchemas.DeviceTypeUpdate):
    db_deviceType = db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.id == deviceType.id).first()

    try:
        if deviceType.type_name is not None:
            db_deviceType.type_name = deviceType.type_name.lower()

        db.commit()
        db.refresh(db_deviceType)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_deviceType

def delete_device(db: Session, deviceType_id: int):
    db_deviceType = db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.id == deviceType_id).first()
    db.delete(db_deviceType)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "DeviceType deleted"})