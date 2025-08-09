# Script para probar el despliegue en Railway
# Reemplaza TU_RAILWAY_URL con tu URL real

param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayUrl
)

Write-Host "🧪 Probando despliegue en Railway..." -ForegroundColor Green
Write-Host "URL: https://$RailwayUrl" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health check
Write-Host "1. Health check:" -ForegroundColor Yellow
try {
    $healthResponse = Invoke-RestMethod -Uri "https://$RailwayUrl/health" -Method Get
    Write-Host "   ✅ Health OK: $($healthResponse.ok)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Health check falló: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test 2: Animalitos
Write-Host "2. Animalitos endpoint:" -ForegroundColor Yellow
try {
    $animalitosResponse = Invoke-RestMethod -Uri "https://$RailwayUrl/animalitos?date=2025-01-15" -Method Get
    Write-Host "   ✅ Animalitos OK: $($animalitosResponse.count) items" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Animalitos falló: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Loterías
Write-Host "3. Loterías endpoint:" -ForegroundColor Yellow
try {
    $loteriasResponse = Invoke-RestMethod -Uri "https://$RailwayUrl/loterias?date=2025-01-15" -Method Get
    Write-Host "   ✅ Loterías OK: $($loteriasResponse.count) items" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Loterías falló: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 ¡Despliegue exitoso!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   - Health: https://$RailwayUrl/health" -ForegroundColor White
Write-Host "   - Animalitos: https://$RailwayUrl/animalitos?date=2025-01-15" -ForegroundColor White
Write-Host "   - Loterías: https://$RailwayUrl/loterias?date=2025-01-15" -ForegroundColor White
Write-Host "   - Docs: https://$RailwayUrl/docs" -ForegroundColor White
Write-Host ""
Write-Host "📊 Monitoreo disponible en Railway Dashboard" -ForegroundColor Yellow
