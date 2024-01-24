#!/usr/bin/env python3
"""Writing strings to Redis """
from typing import Union, Optional, Callable, Any
from uuid import uuid4
import redis


class Cache:
    """Simple cache using Redis; initializes with an empty cache
        and provides a method to store data with a generated key."""
    def __init__(self):
        """Initialize a new Cache instance with an empty Redis cache."""
        # Create an instance of the Redis client
        self._redis = redis.Redis()
        # Flush the Redis database to start with an empty cache
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache with a randomly generated
            key and return the key."""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis using a key and
        optionally apply a conversion function."""
        #data = self._redis.get(key)
        #if data and fn:
        #    data = fn(data)
        #return data
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """Retrieve and decode a UTF-8 string from
        Redis using the specified key."""
        return str(self._redis.get(key)) #self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve an integer from Redis using the specified key."""
        return int(self._redis.get(key)) #self.get(key, fn=int)
