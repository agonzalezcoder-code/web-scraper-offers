from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_generic(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    # 1. Detectar titulos
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)

        if text:
            results.append({
                "tipo": "Titulo",
                "texto": text,
                "enlace": ""
            })

    # 2. Detectar filas de tablas
    for table in soup.find_all("table"):
        headers = [th.get_text(" ", strip=True) for th in table.find_all("th")]
        
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            values = [cell.get_text(" ", strip=True) for cell in cells]
            values = [value for value in values if value]

            if values:
                if headers and len(headers) == len(values):
                    texto_tabla = ", ".join([f"{headers[i]}: {values[i]}" for i in range(len(values))])
                else:
                    texto_tabla = " | ".join(values)

                results.append({
                    "tipo": "Tabla",
                    "texto": texto_tabla,
                    "enlace": ""
                })

    # 3. Detectar elementos de listas
    palabras_basura = {"next", "previous", "siguiente", "anterior", "home", "inicio", "page", "cart", "carrito"}
    
    for item in soup.find_all("li"):
        if item.find(["article", "section", "table", "form"]):
            continue
            
        text = item.get_text(" ", strip=True)

        if text and len(text) < 150:
            palabras_texto = set(text.lower().split())
            
            if palabras_texto.intersection(palabras_basura) or "page " in text.lower():
                continue

            results.append({
                "tipo": "Lista",
                "texto": text,
                "enlace": ""
            })

    # 4. Detectar enlaces
    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True)
        href = link["href"].strip()

        if (
            text
            and href
            and not href.startswith(
                ("javascript:", "mailto:", "tel:")
            )
        ):
            results.append({
                "tipo": "Enlace",
                "texto": text,
                "enlace": urljoin(base_url, href)
            })

        # 5. Detectar tarjetas y datos repetidos (¡Ajustado para Books to Scrape!)
        for tarjeta in soup.find_all("article", class_="product_pod"):
            # En esta página, el título completo está dentro del atributo 'title' del enlace de la imagen o del h3
            enlace_titulo = tarjeta.find("h3").find("a") if tarjeta.find("h3") else None
            
            if enlace_titulo and enlace_titulo.has_attr("title"):
                titulo_texto = enlace_titulo["title"].strip()
            elif enlace_titulo:
                titulo_texto = enlace_titulo.get_text(" ", strip=True)
            else:
                titulo_texto = "Producto desconocido"
            
            # Extraemos el precio usando su clase exacta
            precio_el = tarjeta.find("p", class_="price_color")
            precio_texto = precio_el.get_text(" ", strip=True) if precio_el else "Sin precio"

            # Armamos el texto unificado de la tarjeta
            informacion_tarjeta = f"Libro: {titulo_texto} — Precio: {precio_texto}"
            
            # Conseguimos el enlace individual del libro
            enlace_el = tarjeta.find("a", href=True)
            enlace_url = urljoin(base_url, enlace_el["href"].strip()) if enlace_el else ""

            results.append({
                "tipo": "Tarjeta",
                "texto": informacion_tarjeta,
                "enlace": enlace_url
            })

    return results
