# Loto API

API pública de resultados de loterías venezolanas (Animalitos y Loterías) vía scraping de **loteriadehoy.com**.

## 🚀 API en Producción

**URL Base**: `https://loteria-api-production.up.railway.app`

## 📡 Endpoints

- `GET /health` - Health check
- `GET /animalitos?date=YYYY-MM-DD` - Resultados de animalitos
- `GET /loterias?date=YYYY-MM-DD` - Resultados de loterías
- `GET /metrics` - Métricas de uso

## 📱 Uso en Apps

### JavaScript/React
```javascript
const response = await fetch('https://loteria-api-production.up.railway.app/animalitos?date=2025-01-15');
const data = await response.json();
```

### Flutter/Dart
```dart
final response = await http.get(
  Uri.parse('https://loteria-api-production.up.railway.app/animalitos?date=2025-01-15')
);
final data = json.decode(response.body);
```

## 📊 Respuesta de Ejemplo

```json
{
  "date": "2025-01-15",
  "source": "https://loteriadehoy.com/animalitos/resultados/",
  "count": 149,
  "data": [
    {
      "lottery": "Lotto Activo",
      "items": [
        {
          "time": "08:00 AM",
          "number": "29",
          "animal": "Elefante",
          "image": "https://loteriadehoy.com/dist/files_img/animalitos/elefante.webp"
        }
      ]
    }
  ]
}
```

## ⚡ Características

- **Cache inteligente**: TTL dinámico (fechas pasadas 24h, actual 1h)
- **CORS habilitado**: Para apps web y móviles
- **Métricas**: Monitoreo de uso en tiempo real
- **Documentación**: Swagger UI en `/docs`

## 🔧 Tecnologías

- **FastAPI**: Framework web
- **BeautifulSoup**: Web scraping
- **Railway**: Hosting en la nube
- **Python 3.11**: Runtime
- **Warm cache**: Workflow disponible en `.github/workflows/warm.yml`
