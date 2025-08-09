"""
Script de test para verificar el funcionamiento del sistema de mirror de imágenes.
Ejecuta: python tools/test_mirror.py
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.image_store import mirror_image
from app.settings import CDN_BASE

def test_mirror():
    print("🧪 Testing mirror system...")
    
    # Test 1: Animalitos
    print("\n1. Testing animalitos mirror:")
    animal_url = "https://loteriadehoy.com/dist/files_img/animalitos/caiman.webp"
    animal_result = mirror_image("animalitos", animal_url, "Caimán")
    print(f"   Input: {animal_url}")
    print(f"   Output: {animal_result}")
    print(f"   ✅ Starts with CDN: {animal_result.startswith(CDN_BASE)}")
    
    # Test 2: Loterías
    print("\n2. Testing loterias mirror:")
    lottery_url = "https://loteriadehoy.com/dist/files_img/48-Trio_Activo.webp"
    lottery_result = mirror_image("loterias", lottery_url, "Trio Activo")
    print(f"   Input: {lottery_url}")
    print(f"   Output: {lottery_result}")
    print(f"   ✅ Starts with CDN: {lottery_result.startswith(CDN_BASE)}")
    
    # Test 3: URL relativa
    print("\n3. Testing relative URL:")
    relative_url = "/dist/files_img/animalitos/elefante.webp"
    relative_result = mirror_image("animalitos", relative_url, "Elefante")
    print(f"   Input: {relative_url}")
    print(f"   Output: {relative_result}")
    print(f"   ✅ Starts with CDN: {relative_result.startswith(CDN_BASE)}")
    
    print(f"\n🎯 CDN Base configured: {CDN_BASE}")
    print("✅ Mirror system test completed!")

if __name__ == "__main__":
    test_mirror()
