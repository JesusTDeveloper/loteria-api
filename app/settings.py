# Configuraciones de la aplicación
import os

BASE_URL = os.getenv("LDH_BASE_URL", "https://loteriadehoy.com/")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))  # 1 hora
USER_AGENT = os.getenv("USER_AGENT", "LotoAPI/1.0 (+contacto@tu-dominio.com)")

# --- Imagenes (mirror) ---
MIRROR_IMAGES = os.getenv("MIRROR_IMAGES", "false").lower() == "true"

S3_ENDPOINT   = os.getenv("S3_ENDPOINT", "https://<r2-endpoint>")
S3_BUCKET     = os.getenv("S3_BUCKET", "loto-static")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "")

# Tu CDN/Domain que apunta al bucket (Cloudflare/CloudFront)
CDN_BASE = os.getenv("CDN_BASE", "https://cdn.tudominio.com")
