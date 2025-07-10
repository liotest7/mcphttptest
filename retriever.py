import requests
from bs4 import BeautifulSoup
import json

def clean_html(meta_html):
    soup = BeautifulSoup(meta_html, "html.parser")
    #extract title from article
    title_tag = soup.find("a", class_="NM_Level1_H1")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    #delete all scripts and styles
    for tag in soup(["script", "style"," noscript", "iframe", "svg", "img", "video", "audio","header", "footer", "nav"]):
        tag.decompose()
    
    clean_text = soup.get_text(separator='\n',strip=True)

    return {
        "title": title,
        "text": clean_text
        }

def fetch_articles():
    url = "https://plugins.ninjamock.com/api/v1/articles"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def process_all_articles():
    raw_articles = fetch_articles()
    parsed_articles = []

    for item in raw_articles:
        html_content = item.get("content","")
        if html_content:
            article = clean_html(html_content)
            parsed_articles.append(article)

    return parsed_articles

def save_to_json(parsed_articles, filename="articles.json"):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(parsed_articles, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    articles = process_all_articles()
    save_to_json(articles)
    print(f"Processed {len(articles)} articles and saved to 'articles.json'.")