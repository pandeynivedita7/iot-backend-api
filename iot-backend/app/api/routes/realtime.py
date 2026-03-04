from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.realtime.manager import manager

router = APIRouter(tags=["realtime"])

@router.websocket("/ws/sensors/{sensor_id}")
async def ws_sensor_stream(websocket: WebSocket, sensor_id: str):
    await manager.connect(sensor_id, websocket)
    try:
        while True:
            # keep connection alive; optional: receive pings/messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(sensor_id, websocket)
    except Exception:
        manager.disconnect(sensor_id, websocket)