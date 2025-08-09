#!/usr/bin/env python3
"""
Script simple para probar que las dependencias funcionen
"""
import sys
import os

def test_imports():
    print("Testing imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import httpx
        print(f"✅ Httpx {httpx.__version__}")
    except ImportError as e:
        print(f"❌ Httpx import failed: {e}")
        return False
    
    try:
        import bs4
        print(f"✅ BeautifulSoup4 {bs4.__version__}")
    except ImportError as e:
        print(f"❌ BeautifulSoup4 import failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 All imports successful!")
    else:
        print("\n❌ Some imports failed!")
        sys.exit(1)
