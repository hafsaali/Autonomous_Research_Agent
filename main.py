from fastapi import FastAPI
from config.requests import QueryRequest
from src.search import google_scrape_search, arxiv_search
from utils.scraper import scrape_text_from_url
from src.summarizer import summarize
from src.memory import init_memory

app = FastAPI()


@app.post("/research")
def run_research(payload: QueryRequest):
    query = payload.query

    # Step 1: Gather Sources
    google_results = google_scrape_search(query, max_results=3)
    arxiv_results = arxiv_search(query, max_results=3)

    sources = []
    raw_texts = []

    for item in google_results:
        text = scrape_text_from_url(item["link"])
        if len(text) > 100:
            sources.append(item)
            raw_texts.append(text)

    for item in arxiv_results:
        sources.append(item)
        raw_texts.append(item["summary"])

    memory = init_memory(raw_texts)
    combined_text = "\n\n".join(raw_texts[:5])
    summary = summarize(combined_text)

    return {
        "summary": summary,
        "sources": sources
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
