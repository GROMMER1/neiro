
import requests
from bs4 import BeautifulSoup
from knowledge import load_knowledge, add_fact

WIKI_URL = "https://ru.wikipedia.org/wiki/"

def fetch_from_wikipedia(query):
    try:
        url = WIKI_URL + query.replace(" ", "_")
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        content = soup.find("div", {"class": "mw-parser-output"})
        if content:
            paragraphs = content.find_all("p", recursive=False)
            for p in paragraphs:
                if p.text.strip():
                    return p.text.strip()
        return None
    except Exception:
        return None

def auto_learn(query):
    knowledge = load_knowledge()
    if any(query.lower() in item["prompt"].lower() for item in knowledge):
        return None  # Уже известно

    wiki_info = fetch_from_wikipedia(query)
    if wiki_info:
        add_fact(query, wiki_info)
        return wiki_info
    return None
