# Funciones de caché
import time
from typing import Any, Dict, Tuple
from .settings import CACHE_TTL_SECONDS

_store: Dict[str, Tuple[float, Any]] = {}

def get(key: str):
    now = time.time()
    entry = _store.get(key)
    if not entry: 
        return None
    ts, val = entry
    if now - ts > CACHE_TTL_SECONDS:
        _store.pop(key, None)
        return None
    return val

def set(key: str, val: Any):
    _store[key] = (time.time(), val)
