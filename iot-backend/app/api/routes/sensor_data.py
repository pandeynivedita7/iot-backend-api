from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.sensor import Sensor
from app.models.sensor_data import SensorData
from app.schemas.sensor_data import SensorDataCreate, SensorDataOut
from app.realtime.manager import manager

router = APIRouter(prefix="/sensors", tags=["sensor-data"])

@router.post("/sensors/{sensor_id}/data")
async def add_sensor_data(sensor_id: str, payload: SensorDataCreate, db: Session = Depends(get_db)):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    ts = payload.timestamp or datetime.utcnow()

    row = SensorData(sensor_id=sensor_id, value=payload.value, timestamp=ts)
    db.add(row)
    db.commit()
    db.refresh(row)

    await manager.broadcast(sensor_id, {
        "sensor_id": sensor_id,
        "value": row.value,
        "timestamp": row.timestamp.isoformat()
    })

    return row

@router.get("/{sensor_id}/data", response_model=list[SensorDataOut])
def list_sensor_data(
    sensor_id: str,
    from_ts: datetime = Query(..., alias="from"),
    to_ts: datetime = Query(..., alias="to"),
    db: Session = Depends(get_db),
):
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    return (
        db.query(SensorData)
        .filter(SensorData.sensor_id == sensor_id)
        .filter(SensorData.timestamp >= from_ts)
        .filter(SensorData.timestamp <= to_ts)
        .order_by(SensorData.timestamp.asc())
        .all()
    )

@router.post("/sensors/{sensor_id}/data")
async def create_sensor_data(
    sensor_id: str,
    payload: SensorDataCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 1) create db row
    row = SensorData(
        sensor_id=sensor_id,
        value=payload.value,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    # 2) broadcast AFTER commit (so clients see saved data)
    await manager.broadcast(sensor_id, {
        "id": row.id,
        "sensor_id": row.sensor_id,
        "value": row.value,
        "timestamp": row.timestamp.isoformat() if row.timestamp else None
    })

    return row


