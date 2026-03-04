import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)

    sensors = relationship(
        "Sensor",
        back_populates="device",
        cascade="all, delete-orphan"
    )