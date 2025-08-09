# Script para configurar credenciales de Cloudflare R2
# Ejecutar después de crear el bucket y API token

Write-Host "🎯 Configurando credenciales de Cloudflare R2..." -ForegroundColor Green
Write-Host "" -ForegroundColor White

Write-Host "📋 Por favor, proporciona la información de tu configuración R2:" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White

# Solicitar Account ID
$accountId = Read-Host "🔑 Account ID de Cloudflare (32 caracteres hexadecimales)"
if ($accountId.Length -ne 32) {
    Write-Host "❌ Account ID debe tener exactamente 32 caracteres" -ForegroundColor Red
    exit 1
}

# Solicitar Access Key ID
$accessKeyId = Read-Host "🔑 Access Key ID de R2"
if ($accessKeyId.Length -lt 10) {
    Write-Host "❌ Access Key ID parece ser muy corto" -ForegroundColor Red
    exit 1
}

# Solicitar Secret Access Key (oculto)
$secretAccessKey = Read-Host "🔑 Secret Access Key de R2 (se ocultará mientras escribes)" -AsSecureString
if ($secretAccessKey.Length -eq 0) {
    Write-Host "❌ Secret Access Key no puede estar vacío" -ForegroundColor Red
    exit 1
}

# Convertir SecureString a string
$secretAccessKeyText = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretAccessKey))

# Solicitar CDN Base URL
$cdnBase = Read-Host "🌐 CDN Base URL (ej: https://cdn.tudominio.com o https://pub-1234567890.r2.dev)"
if (-not $cdnBase.StartsWith("https://")) {
    Write-Host "❌ CDN Base URL debe comenzar con https://" -ForegroundColor Red
    exit 1
}

Write-Host "" -ForegroundColor White
Write-Host "🔍 Verificando configuración..." -ForegroundColor Yellow

# Generar contenido del archivo .env
$envContent = @"
# Variables de entorno para Cloudflare R2
# ⚠️  NO COMMITEAR ESTE ARCHIVO AL REPOSITORIO

MIRROR_IMAGES=true
S3_ENDPOINT=https://${accountId}.r2.cloudflarestorage.com
S3_BUCKET=loto-static
S3_ACCESS_KEY=${accessKeyId}
S3_SECRET_KEY=${secretAccessKeyText}
CDN_BASE=${cdnBase}
USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"

# Configuración para Render/Railway:
# MIRROR_IMAGES=true
# S3_ENDPOINT=https://${accountId}.r2.cloudflarestorage.com
# S3_BUCKET=loto-static
# S3_ACCESS_KEY=${accessKeyId}
# S3_SECRET_KEY=${secretAccessKeyText}
# CDN_BASE=${cdnBase}
# USER_AGENT="LotoAPI/1.0 (+contacto@tu-dominio.com)"
"@

# Guardar en archivo .env
$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "" -ForegroundColor White
Write-Host "✅ Credenciales guardadas en .env" -ForegroundColor Green
Write-Host "" -ForegroundColor White

# Mostrar resumen
Write-Host "📊 Resumen de configuración:" -ForegroundColor Cyan
Write-Host "   Account ID: $accountId" -ForegroundColor White
Write-Host "   Access Key ID: $accessKeyId" -ForegroundColor White
Write-Host "   Secret Access Key: [OCULTO]" -ForegroundColor White
Write-Host "   S3 Endpoint: https://${accountId}.r2.cloudflarestorage.com" -ForegroundColor White
Write-Host "   Bucket: loto-static" -ForegroundColor White
Write-Host "   CDN Base: $cdnBase" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "🔧 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Probar conexión: python tools/test_mirror_complete.py" -ForegroundColor White
Write-Host "   2. Configurar variables en Render/Railway" -ForegroundColor White
Write-Host "   3. Desplegar aplicación" -ForegroundColor White
Write-Host "   4. Ejecutar preseed: python tools/preseed_lottery_icons.py" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "🔒 IMPORTANTE:" -ForegroundColor Red
Write-Host "   - Archivo .env NO debe committearse al repositorio" -ForegroundColor Yellow
Write-Host "   - Credenciales deben mantenerse seguras" -ForegroundColor Yellow
Write-Host "   - Configurar variables en plataforma de despliegue" -ForegroundColor Yellow

# Verificar .gitignore
$gitignoreContent = Get-Content ".gitignore" -ErrorAction SilentlyContinue
if ($gitignoreContent -notcontains ".env") {
    Add-Content ".gitignore" "`n# Environment variables`n.env"
    Write-Host "✅ .env agregado a .gitignore" -ForegroundColor Green
} else {
    Write-Host "✅ .env ya está en .gitignore" -ForegroundColor Green
}

Write-Host "" -ForegroundColor White
Write-Host "🎉 ¡Configuración completada! Ahora puedes proceder con el despliegue." -ForegroundColor Green
