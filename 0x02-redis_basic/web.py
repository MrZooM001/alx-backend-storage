#!/usr/bin/env python3
"""Module to implement expiration web cache"""
import requests
from typing import Dict
import time
from functools import wraps

CACHE: Dict[str, str] = {}
MAX_CACHE_SIZE = 1000


def get_page(url: str) -> str:
    if url in CACHE:
        print("Retrieving data from cache: {}".format(url))
        return CACHE[url]
    else:
        print("Retrieving data from web: {}".format(url))
        response = requests.get(url)
        result = response.text
        CACHE[url] = result
        evict_if_needed()
        return result


def evict_if_needed():
    while len(CACHE) > MAX_CACHE_SIZE:
        oldest_key = min(CACHE, key=CACHE.get)
        del CACHE[oldest_key]


def cache_with_expiration(expiration: int):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            url = args[0]
            key = f"count:{url}"
            if key in CACHE:
                count, timestamp = CACHE[key]
                if time.time() - timestamp > expiration:
                    result = func(*args, **kwargs)
                    CACHE[key] = (count + 1, time.time())
                    return result
                else:
                    CACHE[key] = (count + 1, timestamp)
                    return
            else:
                result = func(*args, **kwargs)
                CACHE[key] = (1, time.time())
                return result

        return wrapped

    return decorator
