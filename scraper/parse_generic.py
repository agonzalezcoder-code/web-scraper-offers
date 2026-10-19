
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
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            values = [
                cell.get_text(" ", strip=True)
                for cell in cells
            ]

            values = [value for value in values if value]

            if values:
                results.append({
                    "tipo": "Tabla",
                    "texto": " | ".join(values),
                    "enlace": ""
                })

    # 3. Detectar elementos de listas
    for item in soup.find_all("li"):
        text = item.get_text(" ", strip=True)

        if text:
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

    return results