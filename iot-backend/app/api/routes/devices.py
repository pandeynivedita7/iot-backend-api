from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.device import Device
from app.models.sensor import Sensor
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceOut

router = APIRouter(prefix="/devices", tags=["devices"])

PREDEFINED_SENSORS = ["temperature", "vibration"]

@router.post("", response_model=DeviceOut)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    device = Device(name=payload.name, location=payload.location)
    db.add(device)
    db.flush()  # so device.id exists now

    # auto-create predefined sensors
    for s_type in PREDEFINED_SENSORS:
        db.add(Sensor(device_id=device.id, type=s_type))

    db.commit()
    db.refresh(device)
    return device

@router.put("/{device_id}", response_model=DeviceOut)
def update_device(device_id: str, payload: DeviceUpdate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if payload.name is not None:
        device.name = payload.name
    if payload.location is not None:
        device.location = payload.location

    db.commit()
    db.refresh(device)
    return device

@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/devices")
def create_device(payload: DeviceCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    device = Device(name=payload.name, location=payload.location)
    db.add(device)
    db.flush()  # so device.id exists now

    # auto-create predefined sensors
    for s_type in PREDEFINED_SENSORS:
        db.add(Sensor(device_id=device.id, type=s_type))

    db.commit()
    db.refresh(device)
    return device