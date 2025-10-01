#!/usr/bin/env python3
"""
Web super ligera para mostrar resultados de lotería
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

app = FastAPI(title="Loto Web", version="1.0.0")

# Configuración
API_BASE = "https://loteria-api-production.up.railway.app"

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
                    <input type="date" id="date" value="2025-01-15">
                    <button class="btn" onclick="loadAnimalitos()">🐾 Animalitos</button>
                    <button class="btn" onclick="loadLoterias()">🎲 Loterías</button>
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
            const API_BASE = 'https://loteria-api-production.up.railway.app';
            
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
            
            async function fetchData(endpoint) {
                const date = document.getElementById('date').value;
                const url = `${API_BASE}/${endpoint}?date=${date}`;
                
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error(`Error ${response.status}: ${response.statusText}`);
                    }
                    return await response.json();
                } catch (error) {
                    throw new Error(`Error al cargar datos: ${error.message}`);
                }
            }
            
            function renderResults(data) {
                const resultsDiv = document.getElementById('results');
                
                let html = `
                    <div class="stats">
                        <h3>📊 Estadísticas</h3>
                        <p><strong>Fecha:</strong> ${data.date}</p>
                        <p><strong>Total de resultados:</strong> ${data.count}</p>
                        <p><strong>Fuente:</strong> ${data.source}</p>
                    </div>
                `;
                
                data.data.forEach(lottery => {
                    html += `
                        <div class="lottery-card">
                            <div class="lottery-title">${lottery.lottery}</div>
                            <div class="items-grid">
                    `;
                    
                    lottery.items.forEach(item => {
                        html += `
                            <div class="item">
                                <div class="item-number">${item.number}</div>
                                <div class="item-animal">${item.animal}</div>
                                <div class="item-time">${item.time}</div>
                            </div>
                        `;
                    });
                    
                    html += `
                            </div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
                hideLoading();
            }
            
            async function loadAnimalitos() {
                showLoading();
                try {
                    const data = await fetchData('animalitos');
                    renderResults(data);
                } catch (error) {
                    showError(error.message);
                }
            }
            
            async function loadLoterias() {
                showLoading();
                try {
                    const data = await fetchData('loterias');
                    renderResults(data);
                } catch (error) {
                    showError(error.message);
                }
            }
            
            // Cargar animalitos por defecto
            window.onload = function() {
                loadAnimalitos();
            };
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
