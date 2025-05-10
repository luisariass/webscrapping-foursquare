import os
import time
from .scraper import VenueScraper
from .parser import parse_venues_from_html
from utils.io_utils import save_json, load_json

def obtener_sitios_turisticos(htmls, url, json_file, carpeta_salida="sitios_turisticos"):
    os.makedirs(carpeta_salida, exist_ok=True)
    json_file_path = os.path.join(carpeta_salida, json_file)
    sitios_existentes = []
    urls_existentes = set()
    if os.path.exists(json_file_path):
        try:
            datos_existentes = load_json(json_file_path)
            sitios_existentes = datos_existentes.get("sitios_turisticos", [])
            urls_existentes = set(s["url_sitio"] for s in sitios_existentes)
        except Exception:
            pass

    sitios_list = []
    for html, url_actual in htmls:
        for sitio in parse_venues_from_html(html, url_actual):
            if sitio["url_sitio"] in urls_existentes:
                continue
            sitio["id"] = len(sitios_existentes) + len(sitios_list) + 1
            sitio["fecha_extraccion"] = time.strftime("%Y-%m-%d %H:%M:%S")
            sitios_list.append(sitio)
            urls_existentes.add(sitio["url_sitio"])

    datos = {
        "sitios_turisticos": sitios_existentes + sitios_list,
        "total": len(sitios_existentes) + len(sitios_list),
        "fuente": url,
        "fecha_extraccion": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    save_json(datos, json_file_path)
    print(f"Datos guardados en archivo: {json_file_path}")
    print(f"Se encontraron {len(sitios_list)} sitios nuevos (total {datos['total']})")
    return datos

if __name__ == "__main__":
    urls_archivos = [
        # ("https://es.foursquare.com/explore?mode=url&near=Sincelejo...", "sitios_sincelejo.json"),
    ]
    scraper = VenueScraper(cookies_path="cookies_foursquare.pkl")
    for url, archivo in urls_archivos:
        htmls = scraper.scrape_city(url)
        if htmls:
            obtener_sitios_turisticos(htmls, url, archivo)
        else:
            print(f"No se pudo extraer HTML de {url}")