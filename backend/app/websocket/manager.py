from typing import Dict, Set
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, match_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(match_id, set()).add(websocket)

    def disconnect(self, match_id: str, websocket: WebSocket):
        self.active_connections.get(match_id, set()).discard(websocket)

    async def broadcast(self, match_id: str, message: str):
        connections = self.active_connections.get(match_id, set())
        for ws in list(connections):
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(match_id, ws)

manager = ConnectionManager()
