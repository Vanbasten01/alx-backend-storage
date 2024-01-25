import requests
import redis
import time
from functools import wraps

# Create an instance of the redis.Redis client
client = redis.Redis()

def cache_decorator(fn):
    """Decorator to track access count and cache the result with an expiration time."""
    @wraps(fn)
    def wrapper(url):
        # Create a unique key for the access count based on the URL
        access_count_key = f"count:{url}"

        # Check if the access count key exists in Redis
        if not client.get(access_count_key):
            # If not, set the access count to 1
            client.set(access_count_key, 1)
        else:
            # If the access count key exists, increment the count
            client.incr(access_count_key, 1)

        # Create a unique key for caching based on the URL
        cache_key = f"result:{url}"

        # Check if the result is already cached
        cached_result = client.get(cache_key)
        if cached_result:
            # If cached, return the cached result
            return cached_result.decode("utf-8")

        # If not cached, call the original function and cache the result with a TTL of 10 seconds
        result = fn(url)
        client.setex(cache_key, 10, result)
        return result

    return wrapper

@cache_decorator
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and return it."""
    result = requests.get(url).text
    return result
