import requests

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text
