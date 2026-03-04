from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db  # adjust if your get_db is elsewhere
from app.models.sensor import Sensor
from app.models.device import Device
from app.schemas.sensors import SensorCreate, SensorOut, SensorUpdate

# If you already have auth, keep it; otherwise you can remove Depends(get_current_user)
from app.core.security import get_current_user

router = APIRouter(prefix="/sensors", tags=["sensors"])


@router.post("", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(
    payload: SensorCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    device = db.query(Device).filter(Device.id == payload.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    sensor = Sensor(device_id=payload.device_id, type=payload.type)
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


@router.get("", response_model=list[SensorOut])
def list_sensors(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(Sensor).all()


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=SensorOut)
def update_sensor(
    sensor_id: str,
    payload: SensorUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    if payload.type is not None:
        sensor.type = payload.type

    db.commit()
    db.refresh(sensor)
    return sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(
    sensor_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    db.delete(sensor)
    db.commit()
    return None