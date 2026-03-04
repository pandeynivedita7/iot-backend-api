from pydantic import BaseModel
from typing import Optional, List

class DeviceCreate(BaseModel):
    name: str
    location: Optional[str] = None

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class SensorOut(BaseModel):
    id: str
    type: str

    class Config:
        from_attributes = True

class DeviceOut(BaseModel):
    id: str
    name: str
    location: Optional[str] = None
    sensors: List[SensorOut] = []

    class Config:
        from_attributes = True