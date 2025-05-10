# foursquare_utils.py

import time
import random
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

def iniciar_driver():
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def pausa_humana(min_s=2, max_s=6):
    time.sleep(random.uniform(min_s, max_s))

def guardar_cookies(driver, ruta_archivo="cookies_foursquare.pkl"):
    pickle.dump(driver.get_cookies(), open(ruta_archivo, "wb"))
    print(f"Cookies guardadas en {ruta_archivo}")

def cargar_cookies(driver, ruta_archivo="cookies_foursquare.pkl"):
    try:
        cookies = pickle.load(open(ruta_archivo, "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)
        return True
    except Exception as e:
        print(f"Error al cargar cookies: {e}")
        return False

def crear_sesion_inicial():
    driver = iniciar_driver()
    driver.get("https://es.foursquare.com/login")
    print("1. Por favor, inicia sesión manualmente en Foursquare")
    print("2. Una vez iniciada la sesión correctamente, presiona Enter")
    input("Presiona Enter cuando hayas iniciado sesión...")
    guardar_cookies(driver)
    driver.quit()
    print("Sesión guardada. Ya puedes usar las cookies en tus scraping.")
    
if __name__ == "__main__":
    crear_sesion_inicial()