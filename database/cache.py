import time
import threading

_cache = {}
_lock = threading.Lock()


def get_cached(key, ttl_seconds, fetch_fn):
    now = time.time()
    with _lock:
        if key in _cache:
            ts, data = _cache[key]
            if now - ts < ttl_seconds:
                return data
    data = fetch_fn()
    with _lock:
        _cache[key] = (now, data)
    return data


def invalidate(key=None):
    with _lock:
        if key:
            _cache.pop(key, None)
        else:
            _cache.clear()
