from bs4 import BeautifulSoup
from utils.foursquare_utils import pausa_humana

def parse_venues_from_html(html, url_actual):
    import requests
    soup = BeautifulSoup(html, 'html.parser')
    sitios = []
    for sitio in soup.find_all('div', class_='contentHolder'):
        puntuacion_tag = sitio.find('div', class_='venueScore positive')
        nombre_tag = sitio.find('h2')
        categoria_tag = sitio.find('span', class_='venueDataItem')
        direccion_tag = sitio.find('div', class_='venueAddress')
        nombre_link = nombre_tag.find('a') if nombre_tag else None
        nombre = nombre_link.get_text(strip=True) if nombre_link else (nombre_tag.get_text(strip=True) if nombre_tag else "N/A")
        categoria = categoria_tag.get_text(strip=True).replace('•', '').strip() if categoria_tag else "N/A"
        direccion = direccion_tag.get_text(strip=True) if direccion_tag else "N/A"
        url_sitio_tag = nombre_link if nombre_link else sitio.find('a')
        url_sitio = url_sitio_tag['href'] if url_sitio_tag and url_sitio_tag.has_attr('href') else ""
        if url_sitio.startswith('/'):
            url_sitio = requests.compat.urljoin(url_actual, url_sitio)
        puntuacion = puntuacion_tag.get_text(strip=True) if puntuacion_tag else "N/A"
        sitio_data = {
            "puntuacion": puntuacion,
            "nombre": nombre,
            "categoria": categoria,
            "direccion": direccion,
            "url_sitio": url_sitio,
        }
        sitios.append(sitio_data)
    return sitios

def get_subcategories(driver):
    try:
        menu_btn = driver.find_element("xpath", '//div[contains(@class,"inputs")]//span[contains(@class,"input-default")]')
        menu_btn.click()
        pausa_humana(1, 2)
        subcat_elements = driver.find_elements("xpath", '//div[contains(@class,"dropdownMenu")]//li/a')
        subcats = [elem.text.strip() for elem in subcat_elements if elem.text.strip().lower() != "favoritos"]
        return subcats
    except Exception as e:
        print("No se encontraron subcategorías:", e)
        return []