from app.core.redis import redis_client

def set_match_state(match_id: str, data: dict):
    key = f"match:{match_id}:state"
    redis_client.hset(key, mapping=data)

def get_match_state(match_id: str):
    key = f"match:{match_id}:state"
    return redis_client.hgetall(key)
