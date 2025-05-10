import os
from .scraper import VenueReviewScraper

def extraer_reseñas_por_sitio(lista_json_sitios, carpeta_salida="reseñas_sitios", cookies_path="cookies_foursquare.pkl"):
    scraper = VenueReviewScraper(cookies_path, carpeta_salida)
    scraper.scrape_reviews_for_sites(lista_json_sitios)
    scraper.close()

if __name__ == "__main__":
    carpeta_sitios = "sitios_turisticos"
    lista_json_sitios = [
        os.path.join(carpeta_sitios, archivo)
        for archivo in os.listdir(carpeta_sitios)
        if archivo.endswith(".json")
    ]
    extraer_reseñas_por_sitio(lista_json_sitios)