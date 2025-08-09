# Loto API (MVP)

API pública de resultados (Animalitos y Loterías) vía scraping de **loteriadehoy.com**.

> Uso educativo / demostrativo. Respeta robots.txt y términos del sitio de origen.

## Endpoints

- `GET /health`
- `GET /animalitos?date=YYYY-MM-DD`
- `GET /loterias?date=YYYY-MM-DD`

### Respuestas
- **Animalitos**:
  ```json
  {
    "date": "2025-08-07",
    "source": "https://loteriadehoy.com/animalitos/resultados/",
    "count": 24,
    "data": [
      {
        "lottery": "Lotto Activo",
        "items": [
          { "time": "08:00 AM", "number": "30", "animal": "Caiman", "image": "https://cdn.tudominio.com/animalitos/caiman.webp" }
        ]
      }
    ]
  }
  ```

## Imágenes (mirroring)

- Por defecto `MIRROR_IMAGES=false`: al detectar una imagen nueva, se sube **una sola vez** al bucket R2/S3 y la API devuelve siempre la URL del **CDN**.
- Variables necesarias:
  - `S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`
  - `CDN_BASE` (dominio del CDN apuntando al bucket)
- Preseed opcional de íconos de loterías:
  ```bash
  python tools/preseed_lottery_icons.py
  ```

## Despliegue

### Variables de entorno para producción

```bash
MIRROR_IMAGES=true
S3_ENDPOINT=https://your-r2-endpoint.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=your-access-key
S3_SECRET_KEY=your-secret-key
CDN_BASE=https://cdn.tudominio.com
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
```

### Pasos de despliegue

1. **Configurar bucket**: Crear bucket `loto-static` en R2/S3/B2
2. **Configurar CDN**: Configurar Cloudflare/CloudFront apuntando al bucket
3. **Variables de entorno**: Configurar todas las variables en Render/Railway
4. **Preseed de íconos** (opcional):
   ```bash
   python tools/preseed_lottery_icons.py
   ```
5. **Desplegar**: Push a main branch

### Cache y rendimiento

- **Cache-Control**: `public, max-age=31536000, immutable` (1 año)
- **CDN**: Configurar para cachear `/animalitos/*` y `/loterias/*`
- **Warm cache**: Workflow disponible en `.github/workflows/warm.yml`
