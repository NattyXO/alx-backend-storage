#!/usr/bin/env python3
"""
create a web cache
"""
import redis
import requests

rc = redis.Redis()

def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a URL using requests and caches the result
    with an expiration time of 10 seconds. Tracks how many times the URL
    has been accessed using Redis.
    """
    count_key = f"count:{url}"
    cached_key = f"cached:{url}"
    count = rc.incr(count_key)
    if count == 1:
        # If this is the first time accessing the URL, cache it for 10 seconds
        resp = requests.get(url)
        rc.setex(cached_key, 10, resp.text)
    else:
        # If the URL has been accessed before, retrieve the cached value
        resp = rc.get(cached_key)
        if resp is None:
            # If the cached value has expired or been evicted, fetch the URL again
            resp = requests.get(url)
            rc.setex(cached_key, 10, resp.text)
        else:
            # If the cached value is still valid, return it
            resp = resp.decode()
    return resp

if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com'))
