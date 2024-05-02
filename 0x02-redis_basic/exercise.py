#!/usr/bin/env python3
"""
Module to implement Redis
"""
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Function to count the number of times a method is called.
    It uses Redis to store the count for each method.

    Arguments:
        method (Callable): The method to be decorated.
    """

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """
        The wrapper function that increments the count in Redis and calls the decorated method.

        Arguemtns:
            self (object): The instance of the class.
            *args (tuple): The positional arguments passed to the decorated method.
            **kwargs (dict): The keyword arguments passed to the decorated method.
        """
        key = method.__qualname__
        self._redis.incr(key, 0) + 1
        return method(self, *args, **kwargs)

    return wrapped


def call_history(method: Callable) -> Callable:
    """
    Function to record the input and output of a method in Redis.

    Arguments:
        method (Callable): The method to be decorated.
    """

    @wraps(method)
    def wrapped(self, *args, **kwargs):
        """
        The wrapper function that records the input and output of the decorated method in Redis.

        Arguments:
            self (object): The instance of the class.
            *args (tuple): The positional arguments passed to the decorated method.
            **kwargs (dict): The keyword arguments passed to the decorated method.
        """
        key_func = method.__qualname__
        input_keys = "{}:inputs".format(key_func)
        output_keys = "{}:outputs".format(key_func)
        self._redis.rpush(input_keys, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_keys, str(result))
        return result

    return wrapped


def replay(self, method: Callable) -> None:
    """
    Replays the input and output of a method
    that has been decorated with the `call_history` decorator.

    Arguments:
        method (Callable): The method to be replayed.
        This method should have been decorated with the `call_history` decorator.
    """
    key_func = method.__qualname__
    input_keys = "{}:inputs".format(key_func)
    output_keys = "{}:outputs".format(key_func)
    inputs = self._redis.lrange(input_keys, 0, -1)
    outputs = self._redis.lrange(output_keys, 0, -1)
    print("{} was called {} times:".format(key_func, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(key_func, inp.decode("utf-8"), out.decode("utf-8"))
        )


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
