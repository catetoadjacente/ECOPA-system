import time

_cache = {}


def get_cached(key, ttl_seconds, fetch_fn):
    now = time.time()
    if key in _cache:
        ts, data = _cache[key]
        if now - ts < ttl_seconds:
            return data
    data = fetch_fn()
    _cache[key] = (now, data)
    return data


def invalidate(key=None):
    if key:
        _cache.pop(key, None)
    else:
        _cache.clear()
