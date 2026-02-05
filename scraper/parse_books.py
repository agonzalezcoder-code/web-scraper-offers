from bs4 import BeautifulSoup

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for book in soup.find_all("article", class_="product_pod"):
        books.append({
            "title": book.h3.a["title"],
            "price": book.find("p", class_="price_color").text,
            "link": book.h3.a["href"]
        })

    return books
