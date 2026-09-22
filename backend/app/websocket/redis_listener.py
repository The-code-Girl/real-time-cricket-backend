import asyncio
import json
from app.core.redis import redis_client
from app.websocket.manager import manager

async def redis_subscribe(match_id: str):
    pubsub = redis_client.pubsub()
    channel = f"match:{match_id}:events"
    try:
        pubsub.subscribe(channel)
        while True:
            message = await asyncio.to_thread(pubsub.get_message, timeout=1)
            if message and message["type"] == "message":
                await manager.broadcast(match_id, message["data"])
    except asyncio.CancelledError:
        raise
    finally:
        pubsub.close()
