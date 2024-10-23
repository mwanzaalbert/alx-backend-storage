#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines a Cache class that interacts with a Redis database to store
and retrieve data. The Cache class implements methods to store various data
types (string, bytes, integer, float) and provides functionality to track
method calls and store call histories.

Key features include:
- Storing data with unique keys generated using UUID.
- Retrieving data with type conversion options.
- Counting how many times specific methods have been called using Redis cmds.
- Recording the history of method calls and their inputs and outputs.

Classes:
    - Cache: A class that provides caching functionality with Redis.

Decorators:
    - count_calls: A decorator to count how many times a method is called.
    - call_history: A decorator to store the history of function inputs and
      outputs.

"""

import uuid
from typing import Union, Callable, Optional
from functools import wraps

import redis

# Define type hints as variables
ReturnType = Optional[Union[str, int]]
FnType = Optional[Callable]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The wrapped method that increments call count.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Use the qualified name of the method as the key
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.
    """
    @wraps(method)
    def wrapper(self, *args):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input as a string
        self._redis.rpush(input_key, str(args))

        # Call the original method
        output = method(self, *args)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    # Get the input and output history
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    # Count the number of calls
    call_count = len(inputs)

    # Print the replay information
    print(f"{method.__qualname__} was called {call_count} times:")

    # Iterate over inputs and outputs
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_data.decode('utf-8')})" +
              f" -> {output_data.decode('utf-8')}")


class Cache:
    """
    Cache class for storing and retrieving data using Redis.

    This class provides an interface to interact with a Redis database,
    allowing for the storage, retrieval, and management of cached data.
    It includes methods for tracking method calls and storing the history
    of inputs and outputs for specific methods.

    Key features include:
    - Storing data with a unique key.
    - Retrieving data with optional type conversion.
    - Counting how many times methods are called.
    - Recording the history of method calls.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client for database
                              operations.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The generated key for the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: FnType = None) -> ReturnType:
        """
        Retrieve data from Redis using the key and apply conversion function if
        provided.

        Args:
            key (str): The key for the data to retrieve.
            fn (Optional[Callable]): A function to convert the retrieved data.

        Returns:
            Optional[Union[str, int]]: The converted data, or
                                       None if the key doesn't exist.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis and decode it.

        Args:
            key (str): The key for the data to retrieve.

        Returns:
            Optional[str]: Decoded string, or None if the key doesn't exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key for the data to retrieve.

        Returns:
            Optional[int]: The integer value, or None if the key doesn't exist.
        """
        return self.get(key, int)


if __name__ == "__main__":
    # Writing strings to Redis
    cache = Cache()

    data = b"hello"
    data_key = cache.store(data)
    print(data_key)

    local_redis = redis.Redis()
    print(local_redis.get(data_key))

    # Reading from Redis and recovering original type
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    print("All test cases passed!")

    #   Incrementing values
    cache = Cache()

    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))

    # Storing lists
    cache = Cache()

    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(
        "{}:inputs".format(cache.store.__qualname__), 0, -1)
    outputs = cache._redis.lrange(
        "{}:outputs".format(cache.store.__qualname__), 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
