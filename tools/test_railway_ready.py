"""
Script para verificar que todo esté listo para Railway.
Ejecuta: python tools/test_railway_ready.py
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_railway_ready():
    print("🚀 Verificando preparación para Railway...")
    print("")
    
    # Verificar archivos necesarios
    required_files = [
        "requirements.txt",
        "app/main.py",
        "app/__init__.py",
        "app/models.py",
        "app/scraping.py",
        "app/cache.py",
        "app/settings.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Archivos faltantes:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # Verificar dependencias
    print("\n📦 Verificando dependencias...")
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI no encontrado")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn no encontrado")
        return False
    
    try:
        import httpx
        print(f"✅ Httpx {httpx.__version__}")
    except ImportError:
        print("❌ Httpx no encontrado")
        return False
    
    try:
        import bs4
        print(f"✅ BeautifulSoup4 {bs4.__version__}")
    except ImportError:
        print("❌ BeautifulSoup4 no encontrado")
        return False
    
    try:
        import boto3
        print(f"✅ Boto3 {boto3.__version__}")
    except ImportError:
        print("❌ Boto3 no encontrado")
        return False
    
    # Verificar configuración
    print("\n🔧 Verificando configuración...")
    try:
        from app.settings import BASE_URL, USER_AGENT
        print(f"✅ Settings cargadas")
        print(f"   - BASE_URL: {BASE_URL}")
        print(f"   - USER_AGENT: {USER_AGENT}")
    except Exception as e:
        print(f"❌ Error cargando settings: {e}")
        return False
    
    # Verificar endpoints
    print("\n🌐 Verificando endpoints...")
    try:
        from app.main import app
        print("✅ FastAPI app creada correctamente")
        
        # Verificar rutas
        routes = [route.path for route in app.routes]
        required_routes = ["/health", "/animalitos", "/loterias", "/docs", "/openapi.json"]
        
        for route in required_routes:
            if route in routes:
                print(f"✅ Ruta {route}")
            else:
                print(f"❌ Ruta faltante: {route}")
                return False
                
    except Exception as e:
        print(f"❌ Error verificando endpoints: {e}")
        return False
    
    print("\n🎉 ¡Todo listo para Railway!")
    print("")
    print("📋 Próximos pasos:")
    print("   1. Ir a https://railway.app")
    print("   2. Crear cuenta y conectar GitHub")
    print("   3. Seleccionar repositorio 'lotoapi'")
    print("   4. Click 'Deploy Now'")
    print("   5. Configurar variables de entorno")
    print("   6. Testear endpoints")
    print("")
    print("🔗 URLs de prueba (después del despliegue):")
    print("   - Health: https://tu-app.up.railway.app/health")
    print("   - Animalitos: https://tu-app.up.railway.app/animalitos?date=2025-01-15")
    print("   - Loterías: https://tu-app.up.railway.app/loterias?date=2025-01-15")
    print("   - Docs: https://tu-app.up.railway.app/docs")
    
    return True

if __name__ == "__main__":
    success = test_railway_ready()
    sys.exit(0 if success else 1)
