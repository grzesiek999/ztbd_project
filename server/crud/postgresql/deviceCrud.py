from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from server.models.postgresql import deviceModel
from server.schemas.postgresql import deviceSchemas


# Device CRUD

def get_device_by_id(db: Session, did: int):
    return db.query(deviceModel.Device).filter(deviceModel.Device.device_id == did).first()

def get_devices_by_name(db: Session, name: str):
    return db.query(deviceModel.Device).filter(deviceModel.Device.device_name == name).all()

def get_devices_by_device_type_id(db: Session, dtid: int):
    return db.query(deviceModel.Device).filter(deviceModel.Device.device_type_id == dtid).all()

def create_device(db: Session, device: deviceSchemas.DeviceCreate):
    db_device = device.Device(
        device_name =  device.device_name.lower(),
        device_type_id = device.device_type_id,
        user_id = device.user_id
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def update_device(db: Session, device: deviceSchemas.DeviceUpdate):
    db_device = db.query(deviceModel.Device).filter(deviceModel.Device.device_id == device.device_id).first()

    try:
        if device.device_name is not None:
            db_device.device_name = device.device_name.lower()
        if device.device_type_id is not None:
            db_device.device_type_id = device.device_type_id

        db.commit()
        db.refresh(db_device)
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return False

    return db_device

def delete_device(db: Session, did: int):
    db_device = db.query(deviceModel.Device).filter(deviceModel.Device.device_id == did).first()
    db.delete(db_device)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Device deleted"})