# Archivo principal de la aplicación
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import Optional
import time

from .models import AnimalitosResponse, LoteriasResponse
from .scraping import scrape
from .cache import get, set, get_smart, set_smart

# Métricas simples
_metrics = {
    "total_requests": 0,
    "cache_hits": 0,
    "scrapes": 0,
    "start_time": time.time()
}

app = FastAPI(
    title="Loto API (MVP)",
    version="0.1.0",
    description="""
    API pública de resultados de loterías venezolanas (Animalitos y Loterías).
    
    **Formato de fecha:** YYYY-MM-DD (ejemplo: 2025-01-15)
    
    **Endpoints disponibles:**
    - `/animalitos?date=2025-01-15` - Resultados de animalitos
    - `/loterias?date=2025-01-15` - Resultados de loterías (triples, trío, terminales)
    - `/health` - Health check
    - `/docs` - Esta documentación
    
    **Fuente:** loteriadehoy.com
    """
)

# CORS abierto para consumir desde apps web / Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"]
)

# Middleware para métricas
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Solo contar endpoints de datos
    if request.url.path in ["/animalitos", "/loterias"]:
        _metrics["total_requests"] += 1
    
    # Agregar headers de métricas
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Cache-Hits"] = str(_metrics["cache_hits"])
    response.headers["X-Total-Requests"] = str(_metrics["total_requests"])
    
    return response

@app.get("/")
def root():
    return {"message": "LotoAPI is running!", "status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.get("/metrics")
def metrics():
    """Métricas de uso de la API"""
    uptime = time.time() - _metrics["start_time"]
    cache_hit_rate = (_metrics["cache_hits"] / max(_metrics["total_requests"], 1)) * 100
    
    return {
        "uptime_seconds": int(uptime),
        "total_requests": _metrics["total_requests"],
        "cache_hits": _metrics["cache_hits"],
        "scrapes": _metrics["scrapes"],
        "cache_hit_rate": f"{cache_hit_rate:.1f}%",
        "efficiency": f"{(1 - _metrics['scrapes'] / max(_metrics['total_requests'], 1)) * 100:.1f}%"
    }

@app.get("/test")
def test():
    return {"message": "Test endpoint working!", "status": "success"}

@app.get("/animalitos", response_model=AnimalitosResponse)
def get_animalitos(date: Optional[str] = None):
    """
    Obtener resultados de animalitos para una fecha específica.
    
    **Parámetros:**
    - `date`: Fecha en formato YYYY-MM-DD (ejemplo: 2025-01-15)
    
    **Ejemplos:**
    - Sin fecha: `/animalitos` (usa fecha actual)
    - Con fecha: `/animalitos?date=2025-01-15`
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar caché inteligente
    cache_key = f"animalitos_{date}"
    cached_result = get_smart(cache_key)
    if cached_result:
        _metrics["cache_hits"] += 1
        return cached_result
    
    try:
        _metrics["scrapes"] += 1
        result = scrape("animalitos", date)
        # Guardar en caché inteligente
        set_smart(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo animalitos: {str(e)}")

@app.get("/loterias", response_model=LoteriasResponse)
def get_loterias(date: Optional[str] = None):
    """
    Obtener resultados de loterías para una fecha específica.
    
    **Parámetros:**
    - `date`: Fecha en formato YYYY-MM-DD (ejemplo: 2025-01-15)
    
    **Ejemplos:**
    - Sin fecha: `/loterias` (usa fecha actual)
    - Con fecha: `/loterias?date=2025-01-15`
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar caché inteligente
    cache_key = f"loterias_{date}"
    cached_result = get_smart(cache_key)
    if cached_result:
        _metrics["cache_hits"] += 1
        return cached_result
    
    try:
        _metrics["scrapes"] += 1
        result = scrape("loterias", date)
        # Guardar en caché inteligente
        set_smart(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo loterías: {str(e)}")
