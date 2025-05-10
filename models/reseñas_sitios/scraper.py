from utils.foursquare_utils import iniciar_driver, cargar_cookies, pausa_humana
from .parser import parse_reviews_from_html
from utils.io_utils import save_json, load_json
import os

class VenueReviewScraper:
    def __init__(self, cookies_path, output_dir="reseñas_sitios"):
        self.cookies_path = cookies_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.driver = iniciar_driver()
        cargar_cookies(self.driver, self.cookies_path)

    def scrape_reviews_for_sites(self, site_json_files):
        for json_sitios in site_json_files:
            ciudad = os.path.splitext(os.path.basename(json_sitios))[0].replace("sitios_", "")
            carpeta_ciudad = os.path.join(self.output_dir, ciudad)
            os.makedirs(carpeta_ciudad, exist_ok=True)
            sitios = load_json(json_sitios)["sitios_turisticos"]
            for sitio in sitios:
                self._scrape_reviews_for_site(sitio, carpeta_ciudad)

    def _scrape_reviews_for_site(self, sitio, carpeta_ciudad):
        url_sitio = sitio["url_sitio"]
        nombre_archivo = f"reseñas_sitio_{sitio['nombre'].replace(' ', '_').replace('/', '_')}.json"
        print(f"\nProcesando sitio: {sitio['nombre']}")
        self.driver.get(url_sitio)
        pausa_humana(3, 7)
        if "Sorry! We're having technical difficulties." in self.driver.page_source:
            print("Bloqueo detectado. Pausando scraping por 10 minutos...")
            import time
            time.sleep(600)
            self.driver.refresh()
            pausa_humana(5, 10)
            if "Sorry! We're having technical difficulties." in self.driver.page_source:
                print("El bloqueo persiste. Saltando este sitio.")
                return
        try:
            from selenium.webdriver.common.by import By
            recientes_btn = self.driver.find_element(By.XPATH, '//span[@class="sortLink" and contains(text(), "Recientes")]')
            recientes_btn.click()
            print("    Filtro 'Recientes' clickeado.")
            pausa_humana(2, 5)
        except Exception as e:
            print(f"    Filtro 'Recientes' NO encontrado: {e}")
        reseñas_sitio = parse_reviews_from_html(self.driver.page_source, sitio)
        print(f"  Total reseñas extraídas para {sitio['nombre']}: {len(reseñas_sitio)}")
        path_out = os.path.join(carpeta_ciudad, nombre_archivo)
        save_json(reseñas_sitio, path_out)
        print(f"  Reseñas guardadas en: {path_out}")
        pausa_humana(3, 8)

    def close(self):
        self.driver.quit()