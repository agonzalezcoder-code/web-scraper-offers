from scraper.fetch_page import fetch_html
from scraper.parse_books import parse_books
from scraper.save_data import save_to_csv

URL = "https://books.toscrape.com/"

def main():
    html = fetch_html(URL)
    books = parse_books(html)
    save_to_csv(books, "output/books.csv")
    print("Books scraped successfully!")

if __name__ == "__main__":
    main()
