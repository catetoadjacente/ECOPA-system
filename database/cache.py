import time
import threading

_cache = {}
_lock = threading.Lock()
MAX_CACHE_SIZE = 500


def get_cached(key, ttl_seconds, fetch_fn):
    now = time.time()
    with _lock:
        if key in _cache:
            ts, data = _cache[key]
            if now - ts < ttl_seconds:
                return data
    data = fetch_fn()
    with _lock:
        if len(_cache) >= MAX_CACHE_SIZE:
            _evict_expired()
        _cache[key] = (now, data)
    return data


def _evict_expired():
    """Remove entradas expiradas quando cache atinge limite."""
    now = time.time()
    keys_to_remove = []
    for k, (ts, _) in _cache.items():
        if now - ts > 300:
            keys_to_remove.append(k)
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
