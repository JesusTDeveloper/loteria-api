# Script para configurar despliegue en Railway
# Ejecutar después de crear la cuenta en Railway

Write-Host "🚀 Configurando despliegue en Railway..." -ForegroundColor Green
Write-Host "" -ForegroundColor White

Write-Host "📋 Pasos para desplegar en Railway:" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White

Write-Host "1️⃣ Crear cuenta en Railway:" -ForegroundColor Yellow
Write-Host "   - Ir a https://railway.app" -ForegroundColor White
Write-Host "   - Click 'Start a Project'" -ForegroundColor White
Write-Host "   - Conectar cuenta de GitHub" -ForegroundColor White
Write-Host "   - Autorizar acceso al repositorio" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "2️⃣ Desplegar proyecto:" -ForegroundColor Yellow
Write-Host "   - Seleccionar repositorio 'lotoapi'" -ForegroundColor White
Write-Host "   - Click 'Deploy Now'" -ForegroundColor White
Write-Host "   - Railway detectara Python automaticamente" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "3️⃣ Configurar variables de entorno:" -ForegroundColor Yellow
Write-Host "   - Railway Dashboard → Variables" -ForegroundColor White
Write-Host "   - Agregar estas variables:" -ForegroundColor White
Write-Host "" -ForegroundColor White

# Mostrar variables de entorno
$railwayVars = @"
# Variables basicas para Railway
MIRROR_IMAGES=false
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
CACHE_TTL_SECONDS=300

# Variables opcionales (para R2 mas adelante)
# MIRROR_IMAGES=true
# S3_ENDPOINT=https://TU_ACCOUNT_ID.r2.cloudflarestorage.com
# S3_BUCKET=loto-static
# S3_ACCESS_KEY=TU_ACCESS_KEY_ID
# S3_SECRET_KEY=TU_SECRET_ACCESS_KEY
# CDN_BASE=https://cdn.tudominio.com
"@

Write-Host $railwayVars -ForegroundColor Gray
Write-Host "" -ForegroundColor White

Write-Host "4️⃣ Verificar despliegue:" -ForegroundColor Yellow
Write-Host "   - Esperar que el build termine (2-3 minutos)" -ForegroundColor White
Write-Host "   - Verificar logs en Railway Dashboard" -ForegroundColor White
Write-Host "   - Testear endpoints:" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "5️⃣ URLs de prueba:" -ForegroundColor Yellow
Write-Host "   - Health check: https://tu-app.up.railway.app/health" -ForegroundColor White
Write-Host "   - Animalitos: https://tu-app.up.railway.app/animalitos?date=2025-01-15" -ForegroundColor White
Write-Host "   - Loterias: https://tu-app.up.railway.app/loterias?date=2025-01-15" -ForegroundColor White
Write-Host "   - Docs: https://tu-app.up.railway.app/docs" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "🔧 Comandos de prueba (despues del despliegue):" -ForegroundColor Cyan
Write-Host "   curl https://tu-app.up.railway.app/health" -ForegroundColor White
Write-Host "   curl https://tu-app.up.railway.app/animalitos?date=2025-01-15" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "📊 Monitoreo:" -ForegroundColor Yellow
Write-Host "   - Railway Dashboard → Metrics" -ForegroundColor White
Write-Host "   - Verificar CPU menor a 80%" -ForegroundColor White
Write-Host "   - Verificar Memory menor a 512MB" -ForegroundColor White
Write-Host "   - Verificar Response Time menor a 500ms" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "💰 Planes Railway:" -ForegroundColor Yellow
Write-Host "   - GRATIS: $5 creditos/mes (suficiente para desarrollo)" -ForegroundColor White
Write-Host "   - PRO: $20/mes (para produccion)" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Red
Write-Host "   - Railway se conecta automaticamente a GitHub" -ForegroundColor Yellow
Write-Host "   - Cada push a main desplegara automaticamente" -ForegroundColor Yellow
Write-Host "   - Los logs estan disponibles en Railway Dashboard" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

Write-Host "🎉 ¡Listo para desplegar en Railway!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "📞 Soporte: https://discord.gg/railway" -ForegroundColor Cyan
