import re
import unicodedata
from urllib.parse import urljoin, urlparse

import httpx
import boto3

from .settings import (
    BASE_URL, S3_ENDPOINT, S3_BUCKET,
    S3_ACCESS_KEY, S3_SECRET_KEY, CDN_BASE
)

def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s

def _abs(src: str) -> str:
    if urlparse(src).scheme:
        return src
    return urljoin(BASE_URL, src.lstrip("/"))

def _guess_ext(content_type: str) -> str:
    ct = (content_type or "").lower()
    if "image/webp" in ct: return ".webp"
    if "image/png" in ct:  return ".png"
    if "image/jpeg" in ct: return ".jpg"
    if "image/jpg" in ct:  return ".jpg"
    return ".webp"

def _get_s3_client():
    """Retorna el cliente S3 solo si las credenciales están configuradas correctamente"""
    if (S3_ENDPOINT and S3_ENDPOINT != "https://<r2-endpoint>" and 
        S3_BUCKET and S3_ACCESS_KEY and S3_SECRET_KEY):
        return boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )
    return None

_s3 = _get_s3_client()

def _head(key: str) -> bool:
    if not _s3:
        return False
    try:
        _s3.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except Exception:
        return False

def _put(key: str, body: bytes, content_type: str):
    if not _s3:
        return
    _s3.put_object(
        Bucket=S3_BUCKET, Key=key, Body=body,
        ContentType=content_type, ACL="public-read",
        CacheControl="public, max-age=31536000, immutable"
    )
    # Log de la imagen subida
    kind = key.split('/')[0] if '/' in key else 'unknown'
    print(f"[mirror] uploaded kind={kind} key={key} size={len(body)/1024:.1f}KB")

def mirror_image(kind: str, src: str, name_hint: str) -> str:
    """
    kind: 'loterias' | 'animalitos'
    src: url (abs/rel) de la imagen origen
    name_hint: slug del archivo destino (ej. 'triple_chance' o 'caiman')
    """
    # Si no hay configuración de S3, devolver la URL original
    if not _s3:
        return _abs(src)
    
    src_abs = _abs(src)
    base_key = f"{kind}/{slugify(name_hint)}"

    # prueba extensiones más comunes ya subidas
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        key = base_key + ext
        if _head(key):
            return f"{CDN_BASE}/{key}"

    # descargar y subir
    try:
        with httpx.Client(timeout=20) as c:
            r = c.get(src_abs)
            r.raise_for_status()
            content = r.content
            ct = r.headers.get("Content-Type", "image/webp")
    except Exception as e:
        # Fallback si la descarga falla
        print(f"[mirror] warning: failed to download {src_abs}: {e}")
        return _abs(src)
    
    key = base_key + _guess_ext(ct)
    if not _head(key):
        _put(key, content, ct)
    return f"{CDN_BASE}/{key}"
