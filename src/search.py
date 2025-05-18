import feedparser
import urllib.parse
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/113.0.0.0 Safari/537.36"}


def fetch_snippet_from_url(url, timeout=5):
    """Fetch and extract snippet text from a given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text[:500]  # Short preview
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return ""


def google_scrape_search(query, max_results=5, with_snippets=True):
    """Scrape Google Search results (requires rotating IP/proxy if overused)."""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}&num={max_results}"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] Google scrape failed: {e}")
        return []

    results = []
    raw_results = soup.select(".tF2Cxc")[:max_results]

    for result in raw_results:
        title_elem = result.select_one("h3")
        link_elem = result.select_one(".yuRUbf a")
        if title_elem and link_elem:
            link = link_elem["href"]
            title = title_elem.get_text()
            results.append({"title": title, "url": link})

    # Optional: Fetch and attach snippets in parallel
    if with_snippets:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(fetch_snippet_from_url, r["url"]): r for r in results
            }
            for future in as_completed(futures):
                snippet = future.result()
                futures[future]["snippet"] = snippet

    return results


def arxiv_search(query, max_results=5):
    """Fetch research papers from arXiv."""
    base_url = "http://export.arxiv.org/api/query?"
    encoded_query = urllib.parse.quote(f"all:{query}")
    query_url = f"{base_url}search_query={encoded_query}&start=0&max_results={max_results}"

    try:
        feed = feedparser.parse(query_url)
    except Exception as e:
        print(f"[ERROR] arXiv fetch failed: {e}")
        return []

    return [
        {
            "title": entry.title,
            "summary": entry.summary,
            "url": entry.link
        }
        for entry in feed.entries
    ]
