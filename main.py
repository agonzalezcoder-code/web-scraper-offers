from scraper.fetch_page_selenium import fetch_html_selenium
from scraper.parse_offers import parse_offers
from scraper.filter_offers import filter_best_offers
from scraper.save_data import save_to_csv
from scraper.save_data_json import save_to_json

URL = "https://realpython.github.io/fake-jobs/"

def main():
    html = fetch_html_selenium(URL)
    offers = parse_offers(html)

    save_to_csv(offers, "output/offers.csv")
    save_to_json(offers, "output/offers.json")

    best_offers = filter_best_offers(offers)
    save_to_csv(best_offers, "output/best_offers.csv")
    save_to_json(best_offers, "output/best_offers.json")

    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
