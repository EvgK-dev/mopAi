import redis

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True) 

def set(key, value):
    redis_client.set(key, value)

def get(key):
    return redis_client.get(key)

def exists(key):
    return redis_client.exists(key) > 0

def delete(key):
    redis_client.delete(key)


