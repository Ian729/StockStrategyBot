import feedparser
import json
from pathlib import Path

def load_rss_sources(path='data/rss_sources.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_all_news():
    sources = load_rss_sources()
    all_news = []
    for src in sources:
        feed = feedparser.parse(src['url'])
        for entry in feed.entries[:20]:
            all_news.append({
                'source': src['name'],
                'title': entry.get('title', ''),
                'summary': entry.get('summary', ''),
                'link': entry.get('link', '')
            })
    return all_news

if __name__ == '__main__':
    news = fetch_all_news()
    Path('data/news.json').write_text(json.dumps(news, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Fetched {len(news)} news items.")
