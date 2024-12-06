from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.postgresql import deviceTypeModel
from schemas.postgresql import deviceTypeSchemas


# DeviceType CRUD

def get_device_type_by_id(db: Session, dtid: int):
    return db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.device_type_id == dtid).first()


def get_device_by_type_name(db: Session, type_name: str):
    return db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.type_name == type_name).all()


def create_device(db: Session, deviceType: deviceTypeSchemas.DeviceTypeCreate):
    db_device_type = deviceType.DeviceType(
        type_name =  deviceType.type_name.lower(),
    )

    db.add(db_device_type)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type


def update_device(db: Session, deviceType: deviceTypeSchemas.DeviceTypeUpdate):
    db_device_type = db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.device_type_id == deviceType.device_type_id).first()

    try:
        if deviceType.type_name is not None:
            db_device_type.type_name = deviceType.type_name.lower()

        db.commit()
        db.refresh(db_device_type)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_device_type


def delete_device(db: Session, dtid: int):
    db_device_type = db.query(deviceTypeModel.DeviceType).filter(deviceTypeModel.DeviceType.device_type_id == dtid).first()
    db.delete(db_device_type)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "DeviceType deleted"})