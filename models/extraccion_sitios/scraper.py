from utils.foursquare_utils import iniciar_driver, pausa_humana, cargar_cookies
from parser import parse_venues_from_html, get_subcategories
from utils.io_utils import save_json, load_json
import os
import time

class VenueScraper:
    def __init__(self, cookies_path):
        self.driver = iniciar_driver()
        self.cookies_path = cookies_path

    def login_and_load_cookies(self):
        self.driver.get("https://es.foursquare.com/login")
        pausa_humana(1, 2)
        if not cargar_cookies(self.driver, self.cookies_path):
            self.driver.quit()
            raise RuntimeError("No se pudieron cargar las cookies. Ejecuta crear_sesion_inicial() primero.")
        self.driver.refresh()
        pausa_humana(2, 3)

    def scrape_city(self, url):
        self.login_and_load_cookies()
        self.driver.get(url)
        pausa_humana(2, 4)
        if "login" in self.driver.current_url.lower() or "iniciar sesión" in self.driver.page_source.lower():
            self.driver.quit()
            raise RuntimeError("La sesión no es válida o ha expirado. Ejecuta crear_sesion_inicial() de nuevo.")

        htmls = [self._scrape_full_page()]
        subcats = get_subcategories(self.driver)
        for subcat in subcats:
            htmls.append(self._scrape_subcategory(subcat))
        self.driver.quit()
        return htmls

    def _scrape_full_page(self):
        while True:
            try:
                boton = self.driver.find_element("xpath", '//button[contains(text(), "Ver más resultados")]')
                boton.click()
                pausa_humana(2, 4)
            except:
                break
        return (self.driver.page_source, self.driver.current_url)

    def _scrape_subcategory(self, subcat_name):
        try:
            menu_btn = self.driver.find_element("xpath", '//div[contains(@class,"inputs")]//span[contains(@class,"input-default")]')
            menu_btn.click()
            pausa_humana(1, 2)
            elem = self.driver.find_element("link text", subcat_name)
            elem.click()
            pausa_humana(2, 4)
            while True:
                try:
                    boton = self.driver.find_element("xpath", '//button[contains(text(), "Ver más resultados")]')
                    boton.click()
                    pausa_humana(2, 4)
                except:
                    break
            return (self.driver.page_source, self.driver.current_url)
        except Exception as e:
            print(f"Error al procesar subcategoría {subcat_name}: {e}")
            return None