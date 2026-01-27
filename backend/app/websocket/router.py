from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from app.websocket.manager import manager
from app.websocket.redis_listener import redis_subscribe

router = APIRouter()

@router.websocket("/ws/match/{match_id}")
async def match_socket(websocket: WebSocket, match_id: str):
    await manager.connect(match_id, websocket)

    listener_task = asyncio.create_task(redis_subscribe(match_id))

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(match_id, websocket)
        listener_task.cancel()
