import json
from app.core.redis import redis_client

def publish_match_event(match_id: str, event: dict):
    channel = f"match:{match_id}:events"
    redis_client.publish(channel, json.dumps(event))
