import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")

def search_web(query):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        results = response.json().get("organic", [])
        return results[:3]  # Top 3 for speed
    except Exception:
        return []

def scrape_content(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Clean text extraction
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()

        # Extract meaningful content
        paragraphs = soup.find_all('p')
        clean_text = ' '.join(p.get_text(strip=True) for p in paragraphs if len(p.get_text()) > 40)
        return clean_text.strip()
    except Exception:
        return ""

def summarize_text(text, max_sentences=3):
    sentences = text.split('. ')
    summary = '. '.join(sentences[:max_sentences]).strip()
    return summary + '.' if summary and not summary.endswith('.') else summary

def generate_summary(query):
    search_results = search_web(query)
    summary_blocks = []
    sources = []

    for result in search_results:
        title = result.get("title")
        link = result.get("link")

        content = scrape_content(link)
        if not content:
            continue

        short_summary = summarize_text(content)
        if short_summary:
            summary_blocks.append(f"- {short_summary}")
            sources.append(f"{title}: {link}")

    if not summary_blocks:
        return "Sorry, I couldn't find relevant information right now."

    full_summary = "\n".join(summary_blocks)
    source_list = "\nSources:\n" + "\n".join(sources)

    return f"{full_summary}\n\n{source_list}"
