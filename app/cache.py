# Funciones de caché optimizadas
import time
from datetime import datetime, date
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

def get_smart_ttl(cache_key: str) -> int:
    """
    TTL inteligente basado en la fecha:
    - Fechas pasadas: 24 horas (datos históricos no cambian)
    - Fecha actual: 1 hora (puede haber nuevos resultados)
    """
    try:
        # Extraer fecha del cache_key (formato: "animalitos_2025-01-15")
        if "_" in cache_key:
            date_str = cache_key.split("_", 1)[1]
            cache_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = date.today()
            
            # Si es fecha pasada, cache por 24 horas
            if cache_date < today:
                return 86400  # 24 horas
    except:
        pass
    
    # Fecha actual o error, usar TTL normal
    return CACHE_TTL_SECONDS

def get_smart(key: str):
    """Cache inteligente con TTL dinámico"""
    now = time.time()
    entry = _store.get(key)
    if not entry: 
        return None
    ts, val = entry
    ttl = get_smart_ttl(key)
    if now - ts > ttl:
        _store.pop(key, None)
        return None
    return val

def set_smart(key: str, val: Any):
    """Guardar con TTL inteligente"""
    _store[key] = (time.time(), val)
