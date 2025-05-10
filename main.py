# main.py

import os
from models.extraccion_sitios.modelo_extraccion_sitios import extraer_html_completo_con_cookies, obtener_sitios_turisticos
from models.reseña_usuarios.modelo_reseñas_usuarios import extraer_reseñas_usuarios_unicos
from models.reseñas_sitios.modelo_reseñas_sitios import extraer_reseñas_por_sitio

def flujo_extraccion_sitios(urls_archivos):
    for url, archivo in urls_archivos:
        htmls = extraer_html_completo_con_cookies(url)
        if htmls:
            obtener_sitios_turisticos(htmls, url, archivo)
        else:
            print(f"No se pudo extraer HTML de {url}")

def flujo_reseñas_usuarios():
    carpeta_sitios = "sitios_turisticos"
    lista_json_sitios = [
        os.path.join(carpeta_sitios, archivo)
        for archivo in os.listdir(carpeta_sitios)
        if archivo.endswith(".json")
    ]
    extraer_reseñas_usuarios_unicos(lista_json_sitios)

def flujo_reseñas_sitios():
    carpeta_sitios = "sitios_turisticos"
    lista_json_sitios = [
        os.path.join(carpeta_sitios, archivo)
        for archivo in os.listdir(carpeta_sitios)
        if archivo.endswith(".json")
    ]
    extraer_reseñas_por_sitio(lista_json_sitios)

if __name__ == "__main__":
    # 1. Define tus URLs y archivos de salida aquí
    urls_archivos = [
        ("https://redirect.foursquare.com/explore?mode=url&near=Cartagena%20de%20Indias%2C%20Bol%C3%ADvar&nearGeoId=72057594041615174", "sitios_cartagena.json"),
    ]

    print("=== FLUJO 1: Extracción de sitios turísticos ===")
    flujo_extraccion_sitios(urls_archivos)

    print("\n=== FLUJO 2: Extracción de reseñas de usuarios ===")
    #flujo_reseñas_usuarios()

    print("\n=== FLUJO 3: Extracción de reseñas por sitio ===")
    #flujo_reseñas_sitios()

    print("\nProceso completo.")