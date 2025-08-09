# Script para levantar MinIO localmente
# Ejecutar como administrador si es necesario

Write-Host "🚀 Iniciando MinIO localmente..." -ForegroundColor Green

# Verificar si Docker está disponible
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker encontrado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está disponible. Por favor instala Docker Desktop primero." -ForegroundColor Red
    Write-Host "📥 Descargar desde: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Crear directorio para datos de MinIO
$minioDataPath = "$PWD/minio"
if (-not (Test-Path $minioDataPath)) {
    New-Item -ItemType Directory -Path $minioDataPath -Force
    Write-Host "📁 Directorio creado: $minioDataPath" -ForegroundColor Green
}

# Levantar MinIO
Write-Host "🐳 Levantando MinIO en http://localhost:9000 (API) y http://localhost:9001 (Console)..." -ForegroundColor Yellow

docker run -d --name minio-lotoapi `
  -p 9000:9000 `
  -p 9001:9001 `
  -e MINIO_ROOT_USER=admin `
  -e MINIO_ROOT_PASSWORD=admin123 `
  -v "${minioDataPath}:/data" `
  minio/minio server /data --console-address ":9001"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ MinIO iniciado correctamente!" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "🔗 URLs de acceso:" -ForegroundColor Cyan
    Write-Host "   API: http://localhost:9000" -ForegroundColor White
    Write-Host "   Console: http://localhost:9001" -ForegroundColor White
    Write-Host "   Usuario: admin" -ForegroundColor White
    Write-Host "   Contraseña: admin123" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
    Write-Host "   1. Abrir http://localhost:9001" -ForegroundColor White
    Write-Host "   2. Login con admin/admin123" -ForegroundColor White
    Write-Host "   3. Crear bucket 'loto-static'" -ForegroundColor White
    Write-Host "   4. Configurar como público (solo lectura)" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "🔄 Para detener MinIO: docker stop minio-lotoapi" -ForegroundColor Yellow
} else {
    Write-Host "❌ Error al levantar MinIO" -ForegroundColor Red
}
