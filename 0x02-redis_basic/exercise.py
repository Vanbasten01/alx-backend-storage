#!/usr/bin/env python3
"""Writing strings to Redis """
from typing import Union
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
