import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def get_rivals_news():
    queries = ["Roblox Rivals update news", "Roblox Rivals codes"]
    new_articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for query in queries:
        rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
        try:
            response = requests.get(rss_url, headers=headers, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    new_articles.append({
                        "title": title,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
        except:
            continue
    return new_articles

def update_archive():
    # Fixed News List (No links, just text)
    static_news = [
        {"title": "🔥 NEW CODES! Use '100MVISITS' for a Free Rare Crate and 5,000 Coins! 💰", "date": "2026-04-01"},
        {"title": "🚀 CYBER UPDATE: New 'Neon City' Map is now LIVE! Optimized for 1v1 Snipers! 🏙️⚡", "date": "2026-03-28"},
        {"title": "🏆 SEASON 5 RESET: The Global Leaderboards are OPEN! Can you reach Top 100? ✨", "date": "2026-03-25"},
        {"title": "🔫 NEW BUNDLE: Get the 'Inferno Dragon' Sniper Skin! Limited time only! 🐉🔥", "date": "2026-03-20"},
        {"title": "⚙️ PERFORMANCE PATCH: Fixed lag spikes and improved hit registration! 🛠️✅", "date": "2026-03-15"}
    ]

    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                archive = data.get("articles", [])
        except:
            archive = static_news.copy()
    else:
        archive = static_news.copy()

    fresh_news = get_rivals_news()
    existing_titles = {art['title'] for art in archive}
    
    for news in fresh_news:
        if news['title'] not in existing_titles:
            archive.insert(0, news)

    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles": archive[:25]
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    update_archive()
