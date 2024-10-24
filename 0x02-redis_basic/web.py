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
from typing import Callable
import redis

# Initialize the Redis client
redis_client = redis.Redis()


def cache_page(func):
    """
    Decorator to cache the page result and count accesses.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Track the access count
        count_key = f"count:{url}"

        # Track the access count
        redis_client.incr(count_key)
        print(f"Incremented access count for {url}")  # Debug print

        # Check if the cached result exists
        cached_result = redis_client.get(url)
        if cached_result:
            print("Returning cached content")  # Debug print
            return cached_result.decode('utf-8')

        # Fetch the page content
        print("Fetching new content")  # Debug print
        result = func(url)

        # Cache the result with an expiration time of 10 seconds and
        # return status
        status = redis_client.setex(url, 10, result)
        if status:  # Expecting the status 'OK'
            return "OK"

        # Reset the count each time a new cache entry is created
        # redis_client.set(count_key, 1)

        return result

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/3000"
    count_key = f"count:{url}"

    # Reset the access count manually before running
    # redis_client.delete(count_key)  # Reset access count
    # print("Access count reset.")

    # Fetch and cache the page content
    print(get_page(url))  # First call (should fetch the content and cache it)

    # Check the count of accesses from Redis
    count_key = f"count:{url}"
    print(f"Access count for {url}:" +
          f"{redis_client.get(count_key).decode('utf-8')}")

    # Call again to ensure cached content is returned
    print(get_page(url))  # Second call (should return cached content)

    # Check the count again
    print(f"Access count for {url}:" +
          f"{redis_client.get(count_key).decode('utf-8')}")
