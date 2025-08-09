# Script para configurar variables de entorno para producción
# Ejecutar después de configurar R2 y CDN

Write-Host "🚀 Configurando variables de entorno para producción..." -ForegroundColor Green

# Solicitar información al usuario
Write-Host "" -ForegroundColor White
Write-Host "📋 Por favor, proporciona la siguiente información:" -ForegroundColor Cyan

$accountId = Read-Host "🔑 Account ID de Cloudflare R2"
$accessKeyId = Read-Host "🔑 Access Key ID de R2"
$secretAccessKey = Read-Host "🔑 Secret Access Key de R2 (se ocultará mientras escribes)" -AsSecureString
$cdnBase = Read-Host "🌐 CDN Base URL (ej: https://cdn.tudominio.com)"

# Convertir SecureString a string
$secretAccessKeyText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretAccessKey))

# Generar archivo .env
$envContent = @"
# Variables de entorno para producción
MIRROR_IMAGES=true
S3_ENDPOINT=https://${accountId}.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=${accessKeyId}
S3_SECRET_KEY=${secretAccessKeyText}
CDN_BASE=${cdnBase}
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
"@

# Guardar en archivo .env
$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "" -ForegroundColor White
Write-Host "✅ Variables de entorno guardadas en .env" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Revisar archivo .env" -ForegroundColor White
Write-Host "   2. Configurar variables en Render/Railway" -ForegroundColor White
Write-Host "   3. Desplegar aplicación" -ForegroundColor White
Write-Host "   4. Ejecutar preseed: python tools/preseed_lottery_icons.py" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "🔒 IMPORTANTE: No commitear archivo .env al repositorio" -ForegroundColor Red
Write-Host "   Agregar .env a .gitignore si no existe" -ForegroundColor Yellow

# Verificar si .gitignore existe y agregar .env
if (-not (Test-Path ".gitignore")) {
    New-Item -ItemType File -Name ".gitignore" -Force
    Write-Host "📁 Archivo .gitignore creado" -ForegroundColor Green
}

# Agregar .env a .gitignore si no existe
$gitignoreContent = Get-Content ".gitignore" -ErrorAction SilentlyContinue
if ($gitignoreContent -notcontains ".env") {
    Add-Content ".gitignore" "`n# Environment variables`n.env"
    Write-Host "✅ .env agregado a .gitignore" -ForegroundColor Green
}
