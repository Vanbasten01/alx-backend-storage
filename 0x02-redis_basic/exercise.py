#!/usr/bin/env python3
"""Writing strings to Redis """
from typing import Union, Optional, Callable, Any
from uuid import uuid4
import redis
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a class method."""
    key = method.__qualname__
    
    @wraps(method)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        """Wrapper function that increments a key in Redis for Cache.store"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to track method calls and their inputs/outputs in Redis"""
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Wrapper that records input and output data in Redis lists."""
        input_data = str(args)
        self._redis.rpush(input_key, input_data)
        output_data = method(self, *args)
        self._redis.rpush(output_key, output_data)
        return output_data

    return wrapper



class Cache:
    """Simple cache using Redis; initializes with an empty cache
        and provides a method to store data with a generated key."""
    def __init__(self):
        """Initialize a new Cache instance with an empty Redis cache."""
        # Create an instance of the Redis client
        self._redis = redis.Redis()
        # Flush the Redis database to start with an empty cache
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache with a randomly generated
            key and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis using a key and
        optionally apply a conversion function."""
        data = self._redis.get(key)
        if data and fn:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve and decode a UTF-8 string from
        Redis using the specified key."""
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis using the specified key."""
        return self.get(key, fn=int)
