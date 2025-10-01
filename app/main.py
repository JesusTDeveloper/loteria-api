# Archivo principal de la aplicación
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import Optional

from .models import AnimalitosResponse, LoteriasResponse
from .scraping import scrape
from .cache import get, set

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

@app.get("/")
def root():
    return {"message": "LotoAPI is running!", "status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

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
    
    # Verificar caché
    cache_key = f"animalitos_{date}"
    cached_result = get(cache_key)
    if cached_result:
        return cached_result
    
    try:
        result = scrape("animalitos", date)
        # Guardar en caché
        set(cache_key, result)
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
    
    # Verificar caché
    cache_key = f"loterias_{date}"
    cached_result = get(cache_key)
    if cached_result:
        return cached_result
    
    try:
        result = scrape("loterias", date)
        # Guardar en caché
        set(cache_key, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo loterías: {str(e)}")
