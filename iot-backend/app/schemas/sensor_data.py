from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorDataCreate(BaseModel):
    value: float
    timestamp: Optional[datetime] = None

class SensorDataOut(BaseModel):
    id: str
    sensor_id: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True