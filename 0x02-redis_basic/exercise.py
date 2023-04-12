#!/usr/bin/env python3
'''Writing strings to Redis'''

import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    '''Creates a Cache class'''
    def __init__(self):
        '''Instantiates the Cache class'''
        self._redis = redis.Redis(port=6479)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Generates a random key (e.g. using uuid), stores the input data in
        Redis using the random key and returns the key
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key:str, fn: Optional[Callable]=None) -> Union[str, bytes, None, int, float]:
        '''Retrieves the value stored in Redis using the given key.'''
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str)-> str:
        '''Retrieves the stored value in string format'''
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key:str,)-> int:
        '''Retrieves the stored value in in format'''
        return self.get(key, int)
