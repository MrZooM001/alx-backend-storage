#!/usr/bin/env python3
"""Module to implement expiration web cache"""
import requests
from typing import Dict
import time
from functools import wraps

CACHE: Dict[str, str] = {}
MAX_CACHE_SIZE = 1000


def get_page(url: str) -> str:
    """
    Function to Retrieve the content of a web page from the cache if available,
    otherwise fetches it from the web and stores it in the cache.

    Arguments:
        url (str): The URL of the web page to retrieve.

    Note:
    the requests library is fetching the web page content.
    using a global dictionary (CACHE) to store the fetched content.
    It evicts the least recently used entry using the
    evict_if_needed function if the cache is full.
    """
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
    """
    Function to evict the least recently used entry from the cache
    if it exceeds the maximum cache size.

    This function is called whenever a new entry is added to the cache
    and the cache size exceeds the maximum limit.
    It iterates over the cache dictionary,
    identifies the entry with the earliest timestamp,
    and removes it from the cache.
    """
    while len(CACHE) > MAX_CACHE_SIZE:
        oldest_key = min(CACHE, key=CACHE.get)
        del CACHE[oldest_key]


def cache_expiration(expiration: int):
    """
    Decorator function to add expiration to cached data.

    It takes an expiration time in seconds as an argument.
    and then wraps the decorated function and adds expiration logic to the cache.
    When the decorated function is called, it checks if the cached data is expired.
    If the data is expired, it calls the decorated function to fetch new data and updates the cache.
    If the data is not expired, it returns the cached data.

    Arguments:
        expiration (int): The expiration time in seconds for the cached data.
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            """
            Function to add expiration logic to the cached data.
            It called when the decorated function is invoked.

            Arguments:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.
            """
            url = args[0]
            key = "count:{}".format(url)
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
