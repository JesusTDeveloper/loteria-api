# Archivo principal de la aplicación
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from .scraping import scrape
from .cache import get as cache_get, set as cache_set
from .models import AnimalitosResponse, LoteriasResponse

app = FastAPI(
    title="Loto API (MVP)",
    version="0.1.0",
    description="Resultados vía scraping de LoteriaDeHoy (animalitos y loterías)."
)

# CORS abierto para consumir desde apps web / Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.get("/animalitos", response_model=AnimalitosResponse)
def animalitos(date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    key = f"animalitos:{date}"
    cached = cache_get(key)
    if cached:
        return cached
    data = scrape("animalitos", date)
    cache_set(key, data)
    return JSONResponse(data)

@app.get("/loterias", response_model=LoteriasResponse)
def loterias(date: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    key = f"loterias:{date}"
    cached = cache_get(key)
    if cached:
        return cached
    data = scrape("loterias", date)
    cache_set(key, data)
    return JSONResponse(data)
