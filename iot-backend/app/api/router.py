from fastapi import APIRouter
from app.api.routes.devices import router as devices_router
from app.api.routes.sensor_data import router as sensor_data_router
from app.api.routes.auth import router as auth_router
from app.api.routes.sensors import router as sensors_router  # NEW
from app.api.routes.realtime import router as realtime_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(devices_router)
api_router.include_router(sensors_router)      # NEW
api_router.include_router(sensor_data_router)
api_router.include_router(realtime_router)