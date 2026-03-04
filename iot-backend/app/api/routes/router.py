from fastapi import APIRouter
from app.api.routes.devices import router as devices_router
from app.api.routes.sensor_data import router as sensor_data_router

api_router = APIRouter()
api_router.include_router(devices_router)
api_router.include_router(sensor_data_router)