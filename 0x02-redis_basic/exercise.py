#!/usr/bin/env python3
"""
Redis class
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A system to count how many times methods of the Cache class are called
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A call_history decorator to store the
    history of inputs and outputs for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(func):
    """
    A replay function to display the
    history of calls of a particular
    function.
    """
    cache = redis.Redis()
    func_name = func.__qualname__
    calls = cache.get(func_name)
    try:
        calls = int(calls.decode("utf-8"))
    except Exception:
        calls = 0
    print("{} was called {} times:".format(func_name, calls))
    inputs = cache.lrange(f"{func_name}:inputs", 0, -1)
    outputs = cache.lrange(f"{func_name}:outputs", 0, -1)
    for inp, out in zip(inputs, outputs):
        try:
            inp = inp.decode("utf-8")
        except Exception:
            inp = ""
        try:
            outp = outp.decode("utf-8")
        except Exception:
            outp = ""
        print("{}(*{}) -> {}".format(func_name, inp, outp))


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        A store method that takes a data argument and returns a string
        """
        randomKey = str(uuid4())
        self._redis.set(randomKey, data)
        return randomKey

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        A get method that take a key string argument and
        an optional Callable argument named fn.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        parametrize Cache.get with the correct
        conversion function
        """
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        parametrize Cache.get with the correct
        conversion function
        """
        value = self._redis.get(key)
        return value.decode('utf-8')
