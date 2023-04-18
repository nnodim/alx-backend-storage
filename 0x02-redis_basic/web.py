#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
import requests
import redis
from functools import wraps

r = redis.Redis()


def cache(method):
    """counter decorator"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        cached_key = "cached:" + url
        cached_data = r.get(cached_key)
        if cached_data:
            return cached_data.decode('utf-8')

        count_key = "count:" + url
        html = method(url)

        r.incr(count_key)
        r.set(cached_key, html)
        r.expire(cached_key, 10)
        return html
    return wrapper


@cache
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL and returns it.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
