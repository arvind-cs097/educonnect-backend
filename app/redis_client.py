# redis_client.py
import redis

redis_client = redis.StrictRedis(
    host="localhost",  # This is the IP address of Redis as seen from Windows
    port=6379,
    decode_responses=True  # Automatically decode bytes to string
)
