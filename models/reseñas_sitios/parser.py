from bs4 import BeautifulSoup

def parse_reviews_from_html(html, sitio):
    soup = BeautifulSoup(html, 'html.parser')
    reseñas = soup.select('div.tipContents')
    ids_reseñas = set()
    reseñas_sitio = []
    for tip in reseñas:
        contenido = tip.select_one('div.tipText')
        usuario_tag = tip.select_one('span.userName a')
        usuario_nombre = usuario_tag.get_text(strip=True) if usuario_tag else ""
        perfil_url_usuario = usuario_tag['href'] if usuario_tag and usuario_tag.has_attr('href') else ""
        if perfil_url_usuario.startswith('/'):
            perfil_url_usuario = "https://es.foursquare.com" + perfil_url_usuario
        fecha = tip.select_one('span.tipDate')
        reseña_id = (
            (contenido.get_text(strip=True) if contenido else "") +
            (fecha.get_text(strip=True) if fecha else "") +
            usuario_nombre
        )
        if reseña_id in ids_reseñas:
            continue
        ids_reseñas.add(reseña_id)
        reseña = {
            "usuario": usuario_nombre,
            "contenido": contenido.get_text(strip=True) if contenido else "",
            "fecha_reseña": fecha.get_text(strip=True) if fecha else "",
            "lugar": sitio['nombre'],
            "perfil_url_usuario": perfil_url_usuario,
            "perfil_url": sitio["url_sitio"]
        }
        reseñas_sitio.append(reseña)
    return reseñas_sitio