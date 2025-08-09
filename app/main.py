# Archivo principal de la aplicación
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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

@app.get("/")
def root():
    return {"message": "LotoAPI is running!", "status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

@app.get("/test")
def test():
    return {"message": "Test endpoint working!", "status": "success"}
