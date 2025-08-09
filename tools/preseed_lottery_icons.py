"""
Ejecuta: python tools/preseed_lottery_icons.py
Sube íconos de loterías al bucket usando mirror_image.
Ajusta la lista 'LOTTERIES' con los nombres exactamente como aparecen en <th>.
"""
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.image_store import mirror_image, slugify
from app.settings import BASE_URL

# mapa nombre -> ruta relativa del icono (usa lo que viste en el HTML)
LOTTERIES = {
  "Trio Activo":        "/dist/files_img/48-Trio_Activo.webp",
  "Triple Chance":      "/dist/files_img/48-Triple_Chance.webp",
  "Triple Zulia":       "/dist/files_img/48-Triple_Zulia.webp",
  "Triple Tachira":     "/dist/files_img/48-Triple_Tachira.webp",
  "Triple Caracas":     "/dist/files_img/48-Triple_Caracas.webp",
  "Triple Caliente":    "/dist/files_img/48-Triple_Caliente.webp",
  "Triple Zamorano":    "/dist/files_img/48-Triple_Zamorano.webp",
  "La Ricachona":       "/dist/files_img/48-La_Ricachona.webp",
  "Triple Uneloton":    "/dist/files_img/48-Triple_Uneloton.webp",
  "Triple Centena":     "/dist/files_img/48-Triple_Centena.webp",
  "Terminal Trio":      "/dist/files_img/48-Terminal_Trio.webp",
  "El Terminalito":     "/dist/files_img/48-El_Terminalito.webp",
  "Terminal La Granjita": "/dist/files_img/48-Terminal_La_Granjita.webp",
  "La Ruca":            "/dist/files_img/48-La_Ruca.webp",
}

def main():
    for name, path in LOTTERIES.items():
        url = mirror_image("loterias", path, name)
        print(f"{name}: {url}")

if __name__ == "__main__":
    main()
