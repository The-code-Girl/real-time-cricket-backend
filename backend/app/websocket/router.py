from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from app.websocket.manager import manager
from app.websocket.redis_listener import redis_subscribe

router = APIRouter()
listener_tasks: dict[str, asyncio.Task] = {}

@router.websocket("/ws/match/{match_id}")
async def match_socket(websocket: WebSocket, match_id: str):
    await manager.connect(match_id, websocket)

    listener_task = listener_tasks.get(match_id)
    if listener_task is None or listener_task.done():
        listener_task = asyncio.create_task(redis_subscribe(match_id))
        listener_tasks[match_id] = listener_task

    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(match_id, websocket)
    finally:
        if not manager.has_connections(match_id):
            listener_tasks.pop(match_id, None)
            if not listener_task.done():
                listener_task.cancel()
