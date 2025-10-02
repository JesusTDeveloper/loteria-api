# 🎰 Loto API - Documentación Completa

API pública de resultados de loterías venezolanas (Animalitos y Loterías).

## 📋 Información General

- **Base URL**: `https://loteria-api-production.up.railway.app`
- **Formato de fecha**: `YYYY-MM-DD` (ejemplo: `2025-01-15`)
- **Formato de respuesta**: JSON
- **Fuente de datos**: [loteriadehoy.com](https://loteriadehoy.com)

## 🚀 Endpoints Disponibles

### 1. Health Check
Verifica que la API esté funcionando correctamente.

**Endpoint:** `GET /health`

**Respuesta:**
```json
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00.000Z"
}
```

### 2. Animalitos
Obtiene resultados de animalitos para una fecha específica.

**Endpoint:** `GET /animalitos`

**Parámetros:**
- `date` (opcional): Fecha en formato YYYY-MM-DD. Si no se especifica, usa la fecha actual.

**Ejemplos de uso:**
```
GET /animalitos
GET /animalitos?date=2025-01-15
```

**Respuesta de ejemplo:**
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
        },
        {
          "time": "10:00 AM",
          "number": "15",
          "animal": "Caimán",
          "image": "https://loteriadehoy.com/dist/files_img/animalitos/caiman.webp"
        },
        {
          "time": "12:00 PM",
          "number": "33",
          "animal": "León",
          "image": "https://loteriadehoy.com/dist/files_img/animalitos/leon.webp"
        }
      ]
    },
    {
      "lottery": "Triple Chance",
      "items": [
        {
          "time": "09:00 AM",
          "number": "42",
          "animal": "Jirafa",
          "image": "https://loteriadehoy.com/dist/files_img/animalitos/jirafa.webp"
        },
        {
          "time": "11:00 AM",
          "number": "18",
          "animal": "Mono",
          "image": "https://loteriadehoy.com/dist/files_img/animalitos/mono.webp"
        }
      ]
    }
  ]
}
```

### 3. Loterías
Obtiene resultados de loterías (triples, trío, terminales) para una fecha específica.

**Endpoint:** `GET /loterias`

**Parámetros:**
- `date` (opcional): Fecha en formato YYYY-MM-DD. Si no se especifica, usa la fecha actual.

**Ejemplos de uso:**
```
GET /loterias
GET /loterias?date=2025-01-15
```

**Respuesta de ejemplo:**
```json
{
  "date": "2025-01-15",
  "source": "https://loteriadehoy.com/loterias/resultados/",
  "count": 89,
  "data": [
    {
      "lottery": "Trio Activo",
      "image": "https://loteriadehoy.com/dist/files_img/48-Trio_Activo.webp",
      "items": [
        {
          "time": "08:30 AM",
          "A": "123",
          "B": "456",
          "C": "789",
          "sign": null
        },
        {
          "time": "10:30 AM",
          "A": "234",
          "B": "567",
          "C": "890",
          "sign": null
        }
      ]
    },
    {
      "lottery": "Terminal Caracas",
      "image": "https://loteriadehoy.com/dist/files_img/terminal-caracas.webp",
      "items": [
        {
          "time": "09:30 AM",
          "A": null,
          "B": null,
          "C": null,
          "sign": null,
          "value": "345"
        },
        {
          "time": "11:30 AM",
          "A": null,
          "B": null,
          "C": null,
          "sign": null,
          "value": "678"
        }
      ]
    }
  ]
}
```

### 4. Métricas
Obtiene estadísticas de uso de la API.

**Endpoint:** `GET /metrics`

**Respuesta de ejemplo:**
```json
{
  "uptime_seconds": 3600,
  "total_requests": 150,
  "cache_hits": 120,
  "scrapes": 30,
  "cache_hit_rate": "80.0%",
  "efficiency": "80.0%"
}
```

## 📊 Estructura de Datos

### Animalitos
- **date**: Fecha de los resultados
- **source**: URL fuente de los datos
- **count**: Número total de resultados
- **data**: Array de loterías
  - **lottery**: Nombre de la lotería
  - **items**: Array de resultados
    - **time**: Hora del resultado
    - **number**: Número ganador
    - **animal**: Nombre del animal
    - **image**: URL de la imagen del animal

### Loterías
- **date**: Fecha de los resultados
- **source**: URL fuente de los datos
- **count**: Número total de resultados
- **data**: Array de loterías
  - **lottery**: Nombre de la lotería
  - **image**: URL de la imagen de la lotería
  - **items**: Array de resultados
    - **time**: Hora del resultado
    - **A**: Primer número (para triples)
    - **B**: Segundo número (para triples)
    - **C**: Tercer número (para triples)
    - **sign**: Signo (si aplica)
    - **value**: Valor (para terminales)

## 💻 Ejemplos de Uso

### JavaScript/Fetch
```javascript
// Obtener animalitos para una fecha específica
const fetchAnimalitos = async (date) => {
  try {
    const response = await fetch(`https://loteria-api-production.up.railway.app/animalitos?date=${date}`);
    const data = await response.json();
    console.log(`Total resultados: ${data.count}`);
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
};

// Uso
fetchAnimalitos('2025-01-15');
```

### Python/Requests
```python
import requests

def get_animalitos(date):
    url = f"https://loteria-api-production.up.railway.app/animalitos?date={date}"
    response = requests.get(url)
    return response.json()

# Uso
data = get_animalitos('2025-01-15')
print(f"Total resultados: {data['count']}")
```

### Java/Android (Retrofit)
```java
// Interfaz de API
public interface LotteryApi {
    @GET("animalitos")
    Call<AnimalitosResponse> getAnimalitos(@Query("date") String date);
    
    @GET("loterias")
    Call<LoteriasResponse> getLoterias(@Query("date") String date);
}

// Uso
Retrofit retrofit = new Retrofit.Builder()
    .baseUrl("https://loteria-api-production.up.railway.app/")
    .addConverterFactory(GsonConverterFactory.create())
    .build();

LotteryApi api = retrofit.create(LotteryApi.class);
api.getAnimalitos("2025-01-15").enqueue(new Callback<AnimalitosResponse>() {
    @Override
    public void onResponse(Call<AnimalitosResponse> call, Response<AnimalitosResponse> response) {
        if (response.isSuccessful()) {
            AnimalitosResponse data = response.body();
            // Procesar datos
        }
    }
    
    @Override
    public void onFailure(Call<AnimalitosResponse> call, Throwable t) {
        // Manejar error
    }
});
```

### Kotlin/Android (Coroutines)
```kotlin
// Interfaz de API
interface LotteryApi {
    @GET("animalitos")
    suspend fun getAnimalitos(@Query("date") date: String): AnimalitosResponse
    
    @GET("loterias")
    suspend fun getLoterias(@Query("date") date: String): LoteriasResponse
}

// Uso con Coroutines
class LotteryRepository {
    private val api = Retrofit.Builder()
        .baseUrl("https://loteria-api-production.up.railway.app/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(LotteryApi::class.java)
    
    suspend fun getAnimalitos(date: String): Result<AnimalitosResponse> {
        return try {
            val response = api.getAnimalitos(date)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

## 🔧 Configuración y Uso

### Headers Recomendados
```http
User-Agent: TuApp/1.0
Accept: application/json
```

### Manejo de Errores
La API devuelve códigos de estado HTTP estándar:
- `200`: Éxito
- `400`: Solicitud incorrecta
- `500`: Error interno del servidor

### Límites y Consideraciones
- La API tiene cache inteligente para optimizar el rendimiento
- No hay límites de rate limiting actualmente
- Los datos se actualizan según la disponibilidad en la fuente
- Se recomienda implementar cache local en tu aplicación

## 🌐 Página Web

Visita la página web interactiva en: `https://loteria-api-production.up.railway.app/`

Características:
- ✅ Selector de fecha
- ✅ Pestañas para Animalitos y Loterías
- ✅ Resultados en formato JSON
- ✅ Botón para copiar JSON
- ✅ Tutorial completo para desarrolladores

## 📚 Tutorial Completo

Para más información detallada sobre integración, visita: `https://loteria-api-production.up.railway.app/tutorial`

## 🤝 Soporte

- **GitHub**: [JesusTDeveloper/loteria-api](https://github.com/JesusTDeveloper/loteria-api)
- **Fuente**: [loteriadehoy.com](https://loteriadehoy.com)
- **API Status**: `https://loteria-api-production.up.railway.app/health`

---

**Última actualización**: 2025-01-15  
**Versión**: 1.0.0  
**Desarrollado con**: FastAPI, Python, BeautifulSoup
