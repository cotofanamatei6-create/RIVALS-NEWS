import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def get_rivals_news():
    query = "Roblox Rivals game update news"
    rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
    new_articles = []
    
    try:
        response = requests.get(rss_url, timeout=10)
        # Verificăm dacă răspunsul este valid
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                link = item.find('link').text
                new_articles.append({
                    "title": title,
                    "link": link,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
    except Exception as e:
        print(f"Search error: {e}")
    return new_articles

def update_archive():
    # ȘTIRI FIXE - Ca site-ul să aibă mereu conținut la început
    static_news = [
        {"title": "RIVALS Official Launch: The 1v1 Arena is now open!", "link": "https://roblox.com", "date": "2024-06-25"},
        {"title": "Global Leaderboards: Top players are now visible in-game.", "link": "https://roblox.com", "date": "2024-08-10"},
        {"title": "New Weapon Skins Update: Check the latest bundles!", "link": "https://roblox.com", "date": "2024-09-01"}
    ]

    # 1. Verificăm dacă fișierul news.json există deja
    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                archive = data.get("articles", [])
        except:
            archive = static_news
    else:
        archive = static_news

    # 2. Luăm noutățile de pe internet
    fresh_news = get_rivals_news()
    
    # 3. Adăugăm doar ce este NOU (verificăm titlul să nu fie duplicat)
    existing_titles = {art['title'] for art in archive}
    added_count = 0
    
    for news in fresh_news:
        if news['title'] not in existing_titles:
            archive.insert(0, news) # Punem știrea nouă la început
            added_count += 1

    # 4. Păstrăm maximum 25 de știri în total
    archive = archive[:25]

    # 5. Salvăm totul curat în news.json
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles": archive
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Success! Added {added_count} new items to the archive.")

if __name__ == "__main__":
    update_archive()
