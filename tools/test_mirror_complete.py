"""
Script completo para probar el sistema de mirror con MinIO.
Ejecuta: python tools/test_mirror_complete.py
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.image_store import mirror_image
from app.settings import CDN_BASE, MIRROR_IMAGES

def test_mirror_complete():
    print("🧪 Testing complete mirror system...")
    print(f"🔧 MIRROR_IMAGES: {MIRROR_IMAGES}")
    print(f"🎯 CDN_BASE: {CDN_BASE}")
    
    if not MIRROR_IMAGES:
        print("⚠️  MIRROR_IMAGES=false - usando URLs originales")
        return
    
    # Test 1: Animalitos con URL real
    print("\n1. Testing animalitos mirror (URL real):")
    animal_url = "https://loteriadehoy.com/dist/files_img/animalitos/caiman.webp"
    animal_result = mirror_image("animalitos", animal_url, "Caimán")
    print(f"   Input: {animal_url}")
    print(f"   Output: {animal_result}")
    print(f"   ✅ Starts with CDN: {animal_result.startswith(CDN_BASE)}")
    
    # Test 2: Loterías con URL real
    print("\n2. Testing loterias mirror (URL real):")
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
    
    # Test 4: Verificar logs
    print(f"\n📊 Resumen:")
    print(f"   - CDN Base: {CDN_BASE}")
    print(f"   - Mirror habilitado: {MIRROR_IMAGES}")
    print(f"   - Animalitos CDN: {animal_result.startswith(CDN_BASE)}")
    print(f"   - Loterías CDN: {lottery_result.startswith(CDN_BASE)}")
    print(f"   - Relativa CDN: {relative_result.startswith(CDN_BASE)}")
    
    print("\n✅ Mirror system test completed!")

if __name__ == "__main__":
    test_mirror_complete()
