# modelo_reseñas_usuarios.py

import os
import json
import time
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from utils.foursquare_utils import pausa_humana

def extraer_reseñas_usuarios_unicos(lista_json_sitios, carpeta_salida="reseñas_usuarios", cookies_path="cookies_foursquare.pkl"):
    os.makedirs(carpeta_salida, exist_ok=True)
    usuarios_procesados = set()
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Edge(options=options)
    driver.get("https://es.foursquare.com/login")
    time.sleep(2)
    try:
        cookies = pickle.load(open(cookies_path, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)
        print("Cookies cargadas correctamente.")
    except Exception as e:
        print(f"Error al cargar cookies: {e}")
        driver.quit()
        return

    for json_sitios in lista_json_sitios:
        with open(json_sitios, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        sitios = datos["sitios_turisticos"]

        for sitio in sitios:
            url_sitio = sitio["url_sitio"]
            nombre_archivo = f"reseñas_{sitio['nombre'].replace(' ', '_').replace('/', '_')}.json"
            reseñas_sitio = []

            print(f"\nProcesando sitio: {sitio['nombre']}")
            driver.get(url_sitio)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            perfiles = []
            for user_link in soup.select('span.userName a'):
                perfil_url = user_link['href']
                if perfil_url.startswith('/'):
                    perfil_url = "https://es.foursquare.com" + perfil_url
                if perfil_url not in usuarios_procesados:
                    perfiles.append((user_link.text.strip(), perfil_url))
                    usuarios_procesados.add(perfil_url)
            print(f"Perfiles nuevos encontrados: {len(perfiles)}")

            for nombre_usuario, url_perfil in perfiles:
                print(f"  Usuario: {nombre_usuario}")
                driver.get(url_perfil)
                time.sleep(2)
                try:
                    boton = driver.find_element(By.CSS_SELECTOR, "button.seeAll.blueButton")
                    print("    Botón 'Ver todas las reseñas' encontrado y clickeado.")
                    boton.click()
                    time.sleep(2)
                except Exception as e:
                    print(f"    Botón 'Ver todas las reseñas' NO encontrado: {e}")

                reseñas_usuario = []
                pagina_actual = 1
                while True:
                    soup_user = BeautifulSoup(driver.page_source, 'html.parser')
                    reseñas = soup_user.select('div.tipCard')
                    print(f"    Página {pagina_actual}: {len(reseñas)} reseñas encontradas")
                    for tip in reseñas:
                        contenido = tip.select_one('div.tipContent')
                        usuario = tip.select_one('span.tipUserName')
                        fecha = tip.select_one('span.tipDate.link')
                        lugar = tip.select_one('div.tipVenueInfo')
                        categoria = tip.select_one('div.category')
                        reseña = {
                            "usuario": usuario.get_text(strip=True) if usuario else nombre_usuario,
                            "contenido": contenido.get_text(strip=True) if contenido else "",
                            "fecha": fecha.get_text(strip=True) if fecha else "",
                            "lugar": lugar.get_text(strip=True) if lugar else "",
                            "categoria": categoria.get_text(strip=True) if categoria else "",
                            "perfil_url": url_perfil
                        }
                        reseñas_usuario.append(reseña)
                    try:
                        paginacion = driver.find_elements(By.CSS_SELECTOR, "ul.pages li.paginationComponent")
                        siguiente = None
                        encontrado_actual = False
                        for li in paginacion:
                            clases = li.get_attribute("class")
                            if "active" in clases:
                                encontrado_actual = True
                                continue
                            if encontrado_actual and li.text.strip().isdigit():
                                siguiente = li
                                break
                        if siguiente:
                            siguiente.click()
                            time.sleep(2)
                            pagina_actual += 1
                        else:
                            break
                    except Exception as e:
                        print(f"    No se encontró siguiente página: {e}")
                        break

                print(f"    Total reseñas extraídas para {nombre_usuario}: {len(reseñas_usuario)}")
                reseñas_sitio.extend(reseñas_usuario)
                driver.back()
                time.sleep(2)

            path_out = os.path.join(carpeta_salida, nombre_archivo)
            with open(path_out, 'w', encoding='utf-8') as f:
                json.dump(reseñas_sitio, f, ensure_ascii=False, indent=4)
            print(f"  Reseñas guardadas en: {path_out}")

    driver.quit()

if __name__ == "__main__":
    # Ejemplo de uso
    carpeta_sitios = "sitios_turisticos"
    lista_json_sitios = [
        os.path.join(carpeta_sitios, archivo)
        for archivo in os.listdir(carpeta_sitios)
        if archivo.endswith(".json")
    ]
    extraer_reseñas_usuarios_unicos(lista_json_sitios)