import asyncio
import json
from app.core.redis import redis_client
from app.websocket.manager import ConnectionManager

manager = ConnectionManager()

async def redis_subscribe(match_id: str):
    pubsub = redis_client.pubsub()
    channel = f"match:{match_id}:events"
    pubsub.subscribe(channel)

    loop = asyncio.get_event_loop()

    while True:
        message = await loop.run_in_executor(None, pubsub.get_message)
        if message and message["type"] == "message":
            await manager.broadcast(match_id, message["data"])
        await asyncio.sleep(0.01)
