import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), nullable=False, index=True)
    type = Column(String, nullable=False)

    # ✅ ADD THIS LINE (this is the missing property)
    device = relationship("Device", back_populates="sensors")

    # ✅ keep / add this if you have sensor_data relationship
    data_points = relationship("SensorData", back_populates="sensor", cascade="all, delete-orphan")