
import requests


def fetch_html(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    response.encoding = response.apparent_encoding

    return response.text