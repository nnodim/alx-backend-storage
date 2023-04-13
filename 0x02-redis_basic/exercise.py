#!/usr/bin/env python3
""" Redis class and its methods"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


class Cache:
    """
    A simple cache class using Redis.
    """

    def __init__(self) -> None:
        """
        Initialize the cache with a Redis client.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        A store method that takes a data argument and returns a string
        """
        randomKey = str(uuid4())
        self._redis.set(randomKey, data)
        return randomKey
