# Script para monitorear el estado de la API en Railway
param(
    [string]$Url = "https://web-production-04137.up.railway.app"
)

Write-Host "🔍 Monitoreando API en Railway..." -ForegroundColor Green
Write-Host "URL: $Url" -ForegroundColor Cyan
Write-Host ""

while ($true) {
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] Probando endpoint..." -ForegroundColor Yellow
    
    try {
        # Probar endpoint root primero
        $response = Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 10
        Write-Host "   ✅ API responde correctamente!" -ForegroundColor Green
        Write-Host "   📊 Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
        break
    } catch {
        $errorMsg = $_.Exception.Message
        Write-Host "   ❌ Error: $errorMsg" -ForegroundColor Red
        
        if ($errorMsg -like "*502*") {
            Write-Host "   🔄 Deployment aún en progreso..." -ForegroundColor Yellow
        }
    }
    
    Write-Host "   ⏳ Esperando 30 segundos..." -ForegroundColor Gray
    Start-Sleep -Seconds 30
}

Write-Host ""
Write-Host "🎉 ¡API está funcionando!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   - Root: $Url" -ForegroundColor White
Write-Host "   - Health: $Url/health" -ForegroundColor White
Write-Host "   - Animalitos: $Url/animalitos?date=2025-01-15" -ForegroundColor White
Write-Host "   - Loterías: $Url/loterias?date=2025-01-15" -ForegroundColor White
Write-Host "   - Docs: $Url/docs" -ForegroundColor White
