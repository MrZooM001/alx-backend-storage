#!/usr/bin/env python3
"""
Module to implement Redis
"""
import redis
from typing import Union, Optional, Callable
from uuid import uuid4


class Cache:
    """
    A class used to interact with Redis.

    Attributes:
        _redis (redis.Redis): Private attribure to implmenet
        the Redis client instance.
    """

    def __init__(self):
        """Initializes the Redis client and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis and returns a unique identifier.

        Arguments:
            data (typing.Union[str, bytes, int, float]): The data to be stored.
        """
        id = str(uuid4())
        self._redis.set(id, data)
        return id

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves the data associated with the given key from Redis.
        If a function is provided, it applies to the retrieved data.

        Arguments:
            key (str): The key of the data to be retrieved.
            fn (Optional[Callable]): An optional function to convert
            the data back to the desired format
        """
        value = self._redis.get(key)
        return value if not fn else fn(value)

    def get_str(self, key: str) -> str:
        """
        Retrieves the data associated with the given key from Redis and decodes it as a string.

        Arguments:
            key (str): The key of the data to be retrieved.
        """
        return self._redis.get(key).decode("utf-8")

    def get_int(self, key: str) -> int:
        """
        Retrieves the data associated with the given key from Redis and converts it to an integer.

        Arguments:
        key (str): The key of the data to be retrieved.
        """
        return self._redis.get(key, int)
