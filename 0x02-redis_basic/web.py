#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines a function to fetch HTML content from a specified URL using
the requests module, with caching and access counting implemented using Redis.
The caching mechanism stores the content of the URL for a limited time and
tracks how many times the URL has been accessed.

Key features include:
- Fetching the HTML content of a URL.
- Caching the result in Redis with an expiration time of 10 seconds.
- Tracking the number of times a particular URL has been accessed.
- Using a decorator to encapsulate caching and access counting logic.

Functions:
    - get_page: Fetches the HTML content of a given URL and caches the result.

"""

import requests
from functools import wraps
from typing import Optional, Callable, Union
import redis

# Initialize the Redis client
redis_store = redis.Redis()


def cache_page(func: Callable) -> Callable:
    """
    Decorator to cache the page result and count accesses.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Track the access count
        count_key = f"count:{url}"
        redis_store.incr(count_key)

        # Check if the cached result exists
        cached_result = redis_store.get(url)  # redis.get() returns bytes or None
        if cached_result is not None:
            return cached_result.decode('utf-8')

        # Fetch the page content
        result = func(url)

        # Cache the result with an expiration time of 10 seconds
        redis_store.setex(url, 10, result)
        return result

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    # Simulating a request that returns bytes or str
    response = requests.get(url)
    data: Union[str, bytes] = response.content  # response.content returns bytes

    if isinstance(data, bytes):
        return data.decode('utf-8')  # Decode bytes to string
    return data


# Example usage
if __name__ == "__main__":
    # Simulate slow response
    url = "http://slowwly.robertomurray.co.uk/delay/3000"
    print(get_page(url))  # Fetch and cache the page content
    print(get_page(url))  # Should return cached content
