#!/usr/bin/env python3
"""
Web super ligera para mostrar resultados de lotería
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import Optional
import time

from app.models import AnimalitosResponse, LoteriasResponse
from app.scraping import scrape
from app.cache import get, set, get_smart, set_smart

app = FastAPI(title="Loto Web", version="1.0.0")

# CORS abierto para consumir desde apps web / Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", response_class=HTMLResponse)
async def home():
    """Página principal"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Loto Web - Resultados de Lotería</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .controls {
                padding: 30px;
                background: #f8f9fa;
                border-bottom: 1px solid #e9ecef;
            }
            .date-input {
                display: flex;
                gap: 15px;
                align-items: center;
                justify-content: center;
                flex-wrap: wrap;
            }
            .date-input input {
                padding: 12px 20px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            .date-input input:focus {
                border-color: #667eea;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .btn:hover { transform: translateY(-2px); }
            .content {
                padding: 30px;
            }
            .loading {
                text-align: center;
                padding: 50px;
                color: #666;
            }
            .error {
                background: #f8d7da;
                color: #721c24;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
            }
            .results {
                display: grid;
                gap: 20px;
            }
            .lottery-card {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            .lottery-title {
                font-size: 1.3em;
                font-weight: bold;
                color: #333;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }
            .items-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 15px;
            }
            .item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e9ecef;
            }
            .item-number {
                font-size: 1.5em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 5px;
            }
            .item-animal {
                color: #666;
                font-size: 0.9em;
            }
            .item-time {
                color: #999;
                font-size: 0.8em;
                margin-top: 5px;
            }
            .stats {
                background: #e3f2fd;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .stats h3 {
                color: #1976d2;
                margin-bottom: 10px;
            }
            .json-container {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            .json-container h3 {
                color: #333;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }
            .json-display {
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                line-height: 1.5;
                white-space: pre-wrap;
                word-wrap: break-word;
                max-height: 500px;
                overflow-y: auto;
            }
            @media (max-width: 768px) {
                .date-input { flex-direction: column; }
                .items-grid { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
                .header h1 { font-size: 2em; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎰 Loto Web</h1>
                <p>Resultados de Loterías Venezolanas</p>
            </div>
            
            <div class="controls">
                <div class="date-input">
                    <label for="date">📅 Fecha:</label>
                    <input type="date" id="date" value="">
                    <button class="btn" onclick="loadAnimalitos()">🐾 Animalitos</button>
                    <button class="btn" onclick="loadLoterias()">🎲 Loterías</button>
                    <a href="/tutorial" class="btn" style="text-decoration: none; display: inline-block;">📚 Tutorial API</a>
                </div>
            </div>
            
            <div class="content">
                <div id="loading" class="loading" style="display: none;">
                    ⏳ Cargando resultados...
                </div>
                
                <div id="error" class="error" style="display: none;"></div>
                
                <div id="results"></div>
            </div>
        </div>

        <script>
            // Datos de ejemplo para demostración
            const sampleData = {
                animalitos: {
                    date: "2025-01-15",
                    source: "https://loteriadehoy.com/animalitos/resultados/",
                    count: 12,
                    data: [
                        {
                            lottery: "Lotto Activo",
                            items: [
                                { time: "08:00 AM", number: "29", animal: "Elefante" },
                                { time: "10:00 AM", number: "15", animal: "Caimán" },
                                { time: "12:00 PM", number: "33", animal: "León" },
                                { time: "02:00 PM", number: "07", animal: "Tigre" }
                            ]
                        },
                        {
                            lottery: "Triple Chance",
                            items: [
                                { time: "09:00 AM", number: "42", animal: "Jirafa" },
                                { time: "11:00 AM", number: "18", animal: "Mono" },
                                { time: "01:00 PM", number: "25", animal: "Oso" },
                                { time: "03:00 PM", number: "11", animal: "Panda" }
                            ]
                        }
                    ]
                },
                loterias: {
                    date: "2025-01-15",
                    source: "https://loteriadehoy.com/loterias/resultados/",
                    count: 8,
                    data: [
                        {
                            lottery: "Trio Activo",
                            items: [
                                { time: "08:30 AM", number: "123", animal: "Triple" },
                                { time: "10:30 AM", number: "456", animal: "Triple" },
                                { time: "12:30 PM", number: "789", animal: "Triple" },
                                { time: "02:30 PM", number: "012", animal: "Triple" }
                            ]
                        },
                        {
                            lottery: "Terminal Caracas",
                            items: [
                                { time: "09:30 AM", number: "345", animal: "Terminal" },
                                { time: "11:30 AM", number: "678", animal: "Terminal" },
                                { time: "01:30 PM", number: "901", animal: "Terminal" },
                                { time: "03:30 PM", number: "234", animal: "Terminal" }
                            ]
                        }
                    ]
                }
            };
            
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                document.getElementById('error').style.display = 'none';
            }
            
            function hideLoading() {
                document.getElementById('loading').style.display = 'none';
            }
            
            function showError(message) {
                document.getElementById('error').innerHTML = message;
                document.getElementById('error').style.display = 'block';
                hideLoading();
            }
            
            function renderResults(data) {
                const resultsDiv = document.getElementById('results');
                
                // Mostrar los datos en formato JSON
                const jsonString = JSON.stringify(data, null, 2);
                
                let html = `
                    <div class="stats">
                        <h3>📊 Estadísticas</h3>
                        <p><strong>Fecha:</strong> ${data.date}</p>
                        <p><strong>Total de resultados:</strong> ${data.count}</p>
                        <p><strong>Fuente:</strong> ${data.source}</p>
                        <p><strong>⚠️ Nota:</strong> Datos de ejemplo para demostración</p>
                    </div>
                    <div class="json-container">
                        <h3>📄 Resultados en JSON:</h3>
                        <pre class="json-display">${jsonString}</pre>
                    </div>
                `;
                
                resultsDiv.innerHTML = html;
                hideLoading();
            }
            
            async function loadAnimalitos() {
                showLoading();
                const date = document.getElementById('date').value;
                
                try {
                    const response = await fetch(`/animalitos?date=${date}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    renderResults(data);
                } catch (error) {
                    showError('Error al cargar animalitos: ' + error.message);
                }
            }
            
            async function loadLoterias() {
                showLoading();
                const date = document.getElementById('date').value;
                
                try {
                    const response = await fetch(`/loterias?date=${date}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = await response.json();
                    renderResults(data);
                } catch (error) {
                    showError('Error al cargar loterías: ' + error.message);
                }
            }
            
            // Establecer fecha actual por defecto y cargar animalitos
            window.onload = function() {
                // Establecer fecha actual
                const today = new Date().toISOString().split('T')[0];
                document.getElementById('date').value = today;
                
                // Cargar animalitos por defecto
                loadAnimalitos();
            };
        </script>
    </body>
    </html>
    """

@app.get("/tutorial", response_class=HTMLResponse)
async def tutorial():
    """Tutorial de endpoints para desarrolladores"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tutorial API - Loto Web</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                line-height: 1.6;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .nav {
                background: #f8f9fa;
                padding: 15px 30px;
                border-bottom: 1px solid #e9ecef;
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .nav a {
                color: #667eea;
                text-decoration: none;
                padding: 8px 16px;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .nav a:hover { background: #e3f2fd; }
            .content {
                padding: 30px;
            }
            .section {
                margin-bottom: 40px;
            }
            .section h2 {
                color: #333;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }
            .section h3 {
                color: #555;
                margin: 20px 0 10px 0;
            }
            .endpoint {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                margin: 15px 0;
            }
            .endpoint-title {
                font-weight: bold;
                color: #667eea;
                font-size: 1.1em;
                margin-bottom: 10px;
            }
            .method {
                display: inline-block;
                background: #28a745;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8em;
                margin-right: 10px;
            }
            .url {
                font-family: 'Courier New', monospace;
                background: #e9ecef;
                padding: 8px 12px;
                border-radius: 4px;
                margin: 10px 0;
                word-break: break-all;
            }
            .code-block {
                background: #2d3748;
                color: #e2e8f0;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                margin: 15px 0;
                font-family: 'Courier New', monospace;
            }
            .code-block pre { margin: 0; }
            .response-example {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }
            .android-section {
                background: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            .android-section h3 {
                color: #2e7d32;
                margin-top: 0;
            }
            .note {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
            }
            .note strong { color: #856404; }
            .back-btn {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none;
                margin-bottom: 20px;
                transition: transform 0.2s;
            }
            .back-btn:hover { transform: translateY(-2px); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Tutorial API</h1>
                <p>Guía completa para integrar la API en tu app Android</p>
            </div>
            
            <div class="nav">
                <a href="/">🏠 Inicio</a>
                <a href="#endpoints">📡 Endpoints</a>
                <a href="#android">🤖 Android</a>
                <a href="#ejemplos">💡 Ejemplos</a>
            </div>
            
            <div class="content">
                <a href="/" class="back-btn">← Volver al Inicio</a>
                
                <div class="section" id="endpoints">
                    <h2>📡 Endpoints Disponibles</h2>
                    
                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            Health Check
                        </div>
                        <div class="url">https://loteria-api-production.up.railway.app/health</div>
                        <p>Verifica que la API esté funcionando correctamente.</p>
                        <div class="response-example">
                            <strong>Respuesta:</strong>
                            <pre>{"ok": true, "ts": "2025-01-15T10:30:00.000Z"}</pre>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            Animalitos
                        </div>
                        <div class="url">https://loteria-api-production.up.railway.app/animalitos?date=2025-01-15</div>
                        <p>Obtiene resultados de animalitos para una fecha específica.</p>
                        <div class="response-example">
                            <strong>Parámetros:</strong>
                            <ul>
                                <li><code>date</code> (opcional): Fecha en formato YYYY-MM-DD. Si no se especifica, usa la fecha actual.</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            Loterías
                        </div>
                        <div class="url">https://loteria-api-production.up.railway.app/loterias?date=2025-01-15</div>
                        <p>Obtiene resultados de loterías (triples, trío, terminales) para una fecha específica.</p>
                        <div class="response-example">
                            <strong>Parámetros:</strong>
                            <ul>
                                <li><code>date</code> (opcional): Fecha en formato YYYY-MM-DD. Si no se especifica, usa la fecha actual.</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="endpoint">
                        <div class="endpoint-title">
                            <span class="method">GET</span>
                            Métricas
                        </div>
                        <div class="url">https://loteria-api-production.up.railway.app/metrics</div>
                        <p>Obtiene estadísticas de uso de la API.</p>
                    </div>
                </div>
                
                <div class="section" id="android">
                    <h2>🤖 Integración con Android</h2>
                    
                    <div class="android-section">
                        <h3>📱 Configuración en Android Studio</h3>
                        <p>Para usar la API en tu app Android, necesitas agregar permisos de internet:</p>
                        <div class="code-block">
                            <pre>&lt;!-- AndroidManifest.xml --&gt;
&lt;uses-permission android:name="android.permission.INTERNET" /&gt;</pre>
                        </div>
                    </div>
                    
                    <div class="android-section">
                        <h3>🔧 Dependencias Recomendadas</h3>
                        <p>Agrega estas dependencias a tu <code>build.gradle</code>:</p>
                        <div class="code-block">
                            <pre>// build.gradle (Module: app)
dependencies {
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.11.0'
}</pre>
                        </div>
                    </div>
                </div>
                
                <div class="section" id="ejemplos">
                    <h2>💡 Ejemplos de Código</h2>
                    
                    <h3>🌐 Java/Android (Retrofit)</h3>
                    <div class="code-block">
                        <pre>// 1. Modelo de datos
public class LotteryResponse {
    public String date;
    public String source;
    public int count;
    public List&lt;LotteryData&gt; data;
}

public class LotteryData {
    public String lottery;
    public List&lt;LotteryItem&gt; items;
}

public class LotteryItem {
    public String time;
    public String number;
    public String animal;
    public String image;
}

// 2. Interfaz de API
public interface LotteryApi {
    @GET("animalitos")
    Call&lt;LotteryResponse&gt; getAnimalitos(@Query("date") String date);
    
    @GET("loterias")
    Call&lt;LotteryResponse&gt; getLoterias(@Query("date") String date);
}

// 3. Configuración Retrofit
Retrofit retrofit = new Retrofit.Builder()
    .baseUrl("https://loteria-api-production.up.railway.app/")
    .addConverterFactory(GsonConverterFactory.create())
    .build();

LotteryApi api = retrofit.create(LotteryApi.class);

// 4. Uso en tu Activity/Fragment
api.getAnimalitos("2025-01-15").enqueue(new Callback&lt;LotteryResponse&gt;() {
    @Override
    public void onResponse(Call&lt;LotteryResponse&gt; call, Response&lt;LotteryResponse&gt; response) {
        if (response.isSuccessful()) {
            LotteryResponse data = response.body();
            // Procesar datos
            updateUI(data);
        }
    }
    
    @Override
    public void onFailure(Call&lt;LotteryResponse&gt; call, Throwable t) {
        // Manejar error
        showError("Error al cargar datos: " + t.getMessage());
    }
});</pre>
                    </div>
                    
                    <h3>🐍 Kotlin/Android (Retrofit + Coroutines)</h3>
                    <div class="code-block">
                        <pre>// 1. Modelo de datos (Kotlin)
data class LotteryResponse(
    val date: String,
    val source: String,
    val count: Int,
    val data: List&lt;LotteryData&gt;
)

data class LotteryData(
    val lottery: String,
    val items: List&lt;LotteryItem&gt;
)

data class LotteryItem(
    val time: String,
    val number: String,
    val animal: String,
    val image: String
)

// 2. Interfaz de API
interface LotteryApi {
    @GET("animalitos")
    suspend fun getAnimalitos(@Query("date") date: String): LotteryResponse
    
    @GET("loterias")
    suspend fun getLoterias(@Query("date") date: String): LotteryResponse
}

// 3. Uso con Coroutines
class LotteryRepository {
    private val api = Retrofit.Builder()
        .baseUrl("https://loteria-api-production.up.railway.app/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
        .create(LotteryApi::class.java)
    
    suspend fun getAnimalitos(date: String): Result&lt;LotteryResponse&gt; {
        return try {
            val response = api.getAnimalitos(date)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

// 4. Uso en ViewModel
class LotteryViewModel : ViewModel() {
    private val repository = LotteryRepository()
    
    fun loadAnimalitos(date: String) {
        viewModelScope.launch {
            repository.getAnimalitos(date)
                .onSuccess { data ->
                    _lotteryData.value = data
                }
                .onFailure { error ->
                    _errorMessage.value = error.message
                }
        }
    }
}</pre>
                    </div>
                    
                    <h3>🌐 JavaScript/React Native</h3>
                    <div class="code-block">
                        <pre>// Función para obtener datos
const fetchLotteryData = async (type, date) => {
  try {
    const response = await fetch(
      `https://loteria-api-production.up.railway.app/${type}?date=${date}`
    );
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching lottery data:', error);
    throw error;
  }
};

// Uso en componente
const LotteryScreen = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const loadData = async (type, date) => {
    setLoading(true);
    try {
      const result = await fetchLotteryData(type, date);
      setData(result);
    } catch (error) {
      Alert.alert('Error', 'No se pudieron cargar los datos');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    // Tu UI aquí
  );
};</pre>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Formato de Respuesta</h2>
                    <div class="code-block">
                        <pre>{
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
}</pre>
                    </div>
                </div>
                
                <div class="note">
                    <strong>💡 Consejos importantes:</strong>
                    <ul>
                        <li>La API tiene cache inteligente, las consultas son rápidas</li>
                        <li>Usa fechas en formato YYYY-MM-DD (ISO 8601)</li>
                        <li>Maneja errores de red apropiadamente</li>
                        <li>Considera implementar cache local en tu app</li>
                        <li>La API es gratuita, pero respeta los límites de uso</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/debug/url/{kind}/{date}")
async def debug_url(kind: str, date: str):
    """Debug endpoint para verificar URLs"""
    from app.scraping import build_url
    url = build_url(kind, date)
    return {"kind": kind, "date": date, "url": url}

@app.get("/debug/test-scrape/{kind}/{date}")
async def debug_test_scrape(kind: str, date: str):
    """Debug endpoint para probar scraping"""
    try:
        from app.scraping import scrape
        result = scrape(kind, date)
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}

@app.get("/animalitos", response_model=AnimalitosResponse)
def get_animalitos(date: Optional[str] = None):
    """
    Obtener resultados de animalitos para una fecha específica.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar caché inteligente
    cache_key = f"animalitos_{date}"
    cached_result = get_smart(cache_key)
    if cached_result:
        return cached_result
    
    try:
        result = scrape("animalitos", date)
        # Guardar en caché inteligente
        set_smart(cache_key, result)
        return result
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error obteniendo animalitos: {str(e)}")

@app.get("/loterias", response_model=LoteriasResponse)
def get_loterias(date: Optional[str] = None):
    """
    Obtener resultados de loterías para una fecha específica.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # Verificar caché inteligente
    cache_key = f"loterias_{date}"
    cached_result = get_smart(cache_key)
    if cached_result:
        return cached_result
    
    try:
        result = scrape("loterias", date)
        # Guardar en caché inteligente
        set_smart(cache_key, result)
        return result
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Error obteniendo loterías: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
