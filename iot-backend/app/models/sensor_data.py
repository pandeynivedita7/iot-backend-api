from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base  # adjust if your Base import path is different

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = Column(String, ForeignKey("sensors.id"), nullable=False, index=True)

    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)

    sensor = relationship("Sensor", back_populates="data_points")