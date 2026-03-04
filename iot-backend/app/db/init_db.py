from app.db.base import Base
from app.db.session import engine  # whatever your engine is

# IMPORTANT: import models so SQLAlchemy knows them
from app.models.device import Device
from app.models.sensor import Sensor
from app.models.sensor_data import SensorData

def init_db():
    Base.metadata.create_all(bind=engine)