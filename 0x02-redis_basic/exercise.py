#!/usr/bin/env python3
"""
Writing to, reading from, incrementing, storing and retrieving lists
from redis
"""
import redis
from uuid import uuid4
from typing import Union, Optional, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ 
    A decorator function that store the history of inputs and outputs
    for a particular function
    """
    def wrapper(*args, **kwargs):
        """returns a Callable"""
        key = method.__qualname__
        inputs = key + ":inputs"
        outputs = key + ":outputs"
        self._redis.rpush(inputs, str(args))
        output = methods(*args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return output
    return wrapper

def replay(method: Callable) -> Callable:
    """ Displays the history of calls of a particular function"""
    instance = redis.Redis()
    key = method.__qualname__
    count = instance.get(key)
    inputs = instance.lrange('{}: inputs'.format(key), 0, -1)
    outputs = instance.lrange('{}: outputs'.format(key), 0, -1)
    print("{} was called {} times:".format(key, count))
    for data_in, data_out in zip(inputs, outputs):
        print('{}, (*{}), -> {}'.format(key,
            data_in.decode("utf-8"), data_out.decode("utf-8")))

def count_calls(method: Callable) -> Callable:
    """A decorator function that takes a method and returns a Callable"""
    def wrapper(*args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(*args, **kwargs)
    return wrapper

class Cache():
    """Defines the class Cache"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data:Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store the input data in Redis
        using the random key and return the key
        """
        key = str(uuid4)
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable]=None) -> Union[str, bytes, int, float, None]:
        """
        Reads from Redis and converts the data back to the desired format
        """
        if not self._redis.get(key):
            return None
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))
    def get_str(self, key: str) -> Union[str,int,bytes, float]:
        """An str conversion function that retrieves data in str format"""
        return str(self.get(key, lambda x: x.decode('utf-8')))

    def get_int(self, key: str) -> Union[int,str,float,None,bytes]:
        """An int conversion function that retrieves data in int format"""
        return self.get(key, lambda x: int(x))

