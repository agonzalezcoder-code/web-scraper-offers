from bs4 import BeautifulSoup

def parse_offers(html):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    cards = soup.find_all("div", class_="card-content")

    for card in cards:
        title = card.find("h2").text.strip()
        company = card.find("h3").text.strip()
        location = card.find("p", class_="location").text.strip()

        jobs.append({
            "title": title,
            "company": company,
            "location": location
        })

    return jobs
