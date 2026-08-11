import time
import threading

_cache = {}
_lock = threading.Lock()
_key_locks = {}
_key_locks_lock = threading.Lock()
MAX_CACHE_SIZE = 500


def _get_key_lock(key):
    with _key_locks_lock:
        if key not in _key_locks:
            _key_locks[key] = threading.Lock()
        return _key_locks[key]


def get_cached(key, ttl_seconds, fetch_fn):
    now = time.time()
    with _lock:
        if key in _cache:
            ts, ttl, data = _cache[key]
            if now - ts < ttl:
                return data

    key_lock = _get_key_lock(key)
    with key_lock:
        with _lock:
            if key in _cache:
                ts, ttl, data = _cache[key]
                if now - ts < ttl:
                    return data
        data = fetch_fn()
        with _lock:
            if len(_cache) >= MAX_CACHE_SIZE:
                _evict_expired(now)
            _cache[key] = (time.time(), ttl_seconds, data)
        return data


def _evict_expired(now=None):
    """Remove entradas expiradas quando cache atinge limite."""
    if now is None:
        now = time.time()
    keys_to_remove = [k for k, (ts, ttl, _) in _cache.items() if now - ts > ttl]
    for k in keys_to_remove:
        _cache.pop(k, None)


def invalidate(key=None):
    with _lock:
        if key:
            _cache.pop(key, None)
        else:
            _cache.clear()


def invalidate_prefix(prefix):
    with _lock:
        keys_to_remove = [k for k in _cache if k.startswith(prefix)]
        for k in keys_to_remove:
            _cache.pop(k, None)


def cache_stats():
    """Retorna estatisticas do cache para debug."""
    with _lock:
        return {"size": len(_cache), "max_size": MAX_CACHE_SIZE}
