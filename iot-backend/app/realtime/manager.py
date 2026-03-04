from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.sensor_subscribers: Dict[str, Set[WebSocket]] = {}

    async def connect(self, sensor_id: str, websocket: WebSocket):
        await websocket.accept()
        self.sensor_subscribers.setdefault(sensor_id, set()).add(websocket)

    def disconnect(self, sensor_id: str, websocket: WebSocket):
        if sensor_id in self.sensor_subscribers:
            self.sensor_subscribers[sensor_id].discard(websocket)
            if not self.sensor_subscribers[sensor_id]:
                del self.sensor_subscribers[sensor_id]

    async def broadcast(self, sensor_id: str, message: dict):
        subscribers = self.sensor_subscribers.get(sensor_id, set())
        dead = []
        for ws in subscribers:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(sensor_id, ws)

manager = ConnectionManager()