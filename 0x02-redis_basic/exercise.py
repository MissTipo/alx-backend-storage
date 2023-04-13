#!/usr/bin/env python3
""" Contains the cache class and redis methods"""

import redis
from typing import Union, Callable, Optional

from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator that takes a single method Callable argument and returns a Callable
    """

    @wraps(method)
    def wrapper(*args, **kwargs):

        # result = method(*args, **kwargs)
        key = method.__qualname__
        return method(self, *args, **kwargs)
        # args[0]._redis.incr(key)
        # return result

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to add input parametersand output parameters to
    different lists in redis
    """
    @wraps(method)
    def wrapper(*args, **kwargs):

        key = method.__qualname__
        args[0]._redis.rpush("{}:inputs".format(key), str(args[1:]))
        result = method(*args, **kwargs)
        args[0]._redis.rpush("{}:outputs".format(key), str(result))

        return result
    return wrapper


class Cache:
    """ Defines the Cache class"""

    def __init__(self) -> None:
        """ Instantiates the Ccche class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores input data using generated random key and returns the key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Optional[Callable] = None) -> Union[str,
                                                    bytes,
                                                    int,
                                                    float,
                                                    None]:
        """ Retrieves the value stored in Redis under the given key"""
        if not self._redis.get(key):
            return None

        if fn is None:
            return self._redis.get(key)

        return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """
        Retrieves the redis stored value in str format
        """
        return str(self.get(key, lambda d: d.decode("utf-8")))

    def get_int(self, key: str) -> int:
        """
        Retrieves the redis stored value in int format
        """
        return self.get(key, int)
