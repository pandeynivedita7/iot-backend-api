from pydantic import BaseModel
from typing import Optional


class SensorCreate(BaseModel):
    device_id: str
    type: str


class SensorOut(BaseModel):
    id: str
    device_id: str
    type: str

    class Config:
        from_attributes = True


class SensorUpdate(BaseModel):
    type: Optional[str] = None