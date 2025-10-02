import re
from datetime import datetime
from urllib.parse import urljoin
import httpx
from bs4 import BeautifulSoup
from .settings import BASE_URL, USER_AGENT, MIRROR_IMAGES
# from .image_store import mirror_image, slugify

HEADERS = {"User-Agent": USER_AGENT}

# Alias para normalizar nombres de animales
ANIMAL_ALIASES = {
    "Zebra": "Cebra",
    "Ciempies": "Ciempiés",
    "Ciempie": "Ciempiés",
    "Caiman": "Caimán",
    "Aguila": "Águila",
    "Arana": "Araña",
    "Delfin": "Delfín",
    "Leon": "León",
    "Pajaro": "Pájaro",
    "Raton": "Ratón"
}

def normalize_animal(name: str) -> str:
    """Normaliza el nombre del animal usando aliases"""
    return ANIMAL_ALIASES.get(name.strip(), name.strip())

def _abs(url: str) -> str:
    return urljoin(BASE_URL, url) if url else url

def _get_html(url: str) -> str:
    try:
        with httpx.Client(headers=HEADERS, timeout=30) as c:
            r = c.get(url, follow_redirects=True)
            r.raise_for_status()
            return r.text
    except httpx.HTTPError as e:
        raise Exception(f"Error HTTP al obtener {url}: {str(e)}")
    except httpx.TimeoutException:
        raise Exception(f"Timeout al obtener {url}")
    except Exception as e:
        raise Exception(f"Error inesperado al obtener {url}: {str(e)}")

def build_url(kind: str, date_iso: str) -> str:
    if kind == "animalitos":
        return urljoin(BASE_URL, f"animalitos/resultados/{date_iso}/")
    if kind == "loterias":
        return urljoin(BASE_URL, f"loterias/resultados/{date_iso}/")
    raise ValueError("kind inválido")

# ------------ Animalitos ------------
def parse_animalitos(html: str, date_iso: str):
    soup = BeautifulSoup(html, "lxml")
    data, total = [], 0

    for title_block in soup.select("div.title-center"):
        h3 = title_block.find("h3")
        if not h3:
            continue
        lottery = h3.get_text(" ", strip=True) or ""
        if not lottery:
            continue

        nxt = title_block.find_next_sibling(
            lambda t: getattr(t, "name", None) == "div" and "js-con" in (t.get("class") or [])
        ) or title_block.find_next("div", class_=lambda c: c and "js-con" in c.split())
        if not nxt:
            continue

        items = []
        # Cada tarjeta: div.col-... -> .circle (con IMG) + .circle-legend (H4 "num animal", H5 "hora")
        for card in nxt.select("div[class*='col-']"):
            legend = card.select_one(".circle-legend")
            if not legend:
                continue
            h4, h5 = legend.find("h4"), legend.find("h5")
            if not h4 or not h5:
                continue

            # Primero extraer el nombre del animal
            txt = h4.get_text(" ", strip=True)
            m = re.match(r"^\s*(\d+)\s+(.+?)\s*$", txt)
            if m:
                number, animal = m.group(1), m.group(2)
            else:
                parts = txt.split()
                if not parts or not parts[0].isdigit():
                    continue
                number = parts[0]
                animal = " ".join(parts[1:]) if len(parts) > 1 else ""

            # Imagen del animal: dentro de .circle img (la primera)
            circle_img = None
            circle = card.select_one(".circle")
            if circle:
                img_tag = circle.find("img")
                if img_tag and img_tag.get("src"):
                    raw_src = img_tag["src"]
                    # Simplificado: usar URL absoluta directamente
                    circle_img = _abs(raw_src)

            time = h5.get_text(" ", strip=True)

            items.append({
                "time": time,
                "number": number,
                "animal": animal,
                "image": circle_img,  # <- aquí
            })

        if items:
            data.append({"lottery": lottery, "items": items})
            total += len(items)

    return {
        "date": date_iso,
        "source": urljoin(BASE_URL, "animalitos/resultados/"),
        "count": total,
        "data": data
    }

# ------------ Loterías (triples, trío, terminales) ------------
def parse_loterias(html: str, date_iso: str):
    soup = BeautifulSoup(html, "lxml")
    data, total = [], 0

    def _looks_time(s: str) -> bool:
        return bool(re.fullmatch(r"\d{1,2}:\d{2}\s*(AM|PM)", s, flags=re.I))

    for table in soup.select("table.resultados"):
        th = table.find("th")
        if not th:
            continue
        # Nombre + imagen del header
        lottery = th.get_text(" ", strip=True)
        img_tag = th.find("img")
        lottery_img = None
        if img_tag and img_tag.get("src"):
            raw_src = img_tag["src"]
            # Simplificado: usar URL absoluta directamente
            lottery_img = _abs(raw_src)
        if not lottery:
            continue

        tbody = table.find("tbody")
        if not tbody:
            continue

        items = []

        # Terminales: dos filas "Horario" y "Resultados" (tr.ingrid)
        ingrid_rows = tbody.select("tr.ingrid")
        if ingrid_rows:
            hours_row = next((r for r in ingrid_rows if r.find("td", class_="hora") and "Horario" in r.find("td", class_="hora").get_text()), None)
            vals_row  = next((r for r in ingrid_rows if r.find("td", class_="hora") and "Resultados" in r.find("td", class_="hora").get_text()), None)
            if hours_row and vals_row:
                hours = [td.get_text(" ", strip=True) for td in hours_row.find_all("td")[1:]]
                vals  = [td.get_text(" ", strip=True) for td in vals_row.find_all("td")[1:]]
                for h, v in zip(hours, vals):
                    if _looks_time(h) and v:
                        items.append({"time": h, "A": None, "B": None, "C": None, "sign": None, "value": v})

        # Triples / Trío
        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            cells = [td.get_text(" ", strip=True) for td in tds]
            time = cells[0].strip()
            if not _looks_time(time):
                continue

            rest = [c for c in cells[1:] if c != ""]
            nums, sign = [], None
            for c in rest:
                c2 = c.replace("\xa0", " ").strip()
                if re.fullmatch(r"\d{1,3}", c2):
                    nums.append(c2)
                elif len(c2) == 3 and c2.isalpha():
                    sign = c2

            A = nums[0] if len(nums) >= 1 else None
            B = nums[1] if len(nums) >= 2 else None
            C = nums[2] if len(nums) >= 3 else None

            if A or B or C or sign:
                items.append({"time": time, "A": A, "B": B, "C": C, "sign": sign})

        if items:
            seen, dedup = set(), []
            for it in items:
                key = (it.get("time"), it.get("A"), it.get("B"), it.get("C"), it.get("sign"), it.get("value"))
                if key not in seen:
                    seen.add(key)
                    dedup.append(it)
            data.append({"lottery": lottery, "image": lottery_img, "items": dedup})
            total += len(dedup)

    return {
        "date": date_iso,
        "source": urljoin(BASE_URL, "loterias/resultados/"),
        "count": total,
        "data": data
    }

# ------------ Orquestador ------------
def scrape(kind: str, date_iso: str):
    url = build_url(kind, date_iso)
    html = _get_html(url)
    if kind == "animalitos":
        return parse_animalitos(html, date_iso)
    elif kind == "loterias":
        return parse_loterias(html, date_iso)
    else:
        raise ValueError("kind inválido")
