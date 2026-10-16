
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def parse_books(html, base_url="https://books.toscrape.com/"):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.find_all("article", class_="product_pod"):
        books.append({
            "title": book.h3.a["title"],
            "price": book.find("p", class_="price_color").get_text(strip=True),
            "link": urljoin(base_url, book.h3.a["href"])
        })

    return books