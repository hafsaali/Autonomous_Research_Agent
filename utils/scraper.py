from bs4 import BeautifulSoup
import requests

def scrape_text_from_url(url, max_chars=3000):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        return text.strip().replace("\n", " ")[:max_chars]
    except Exception:
        return ""
