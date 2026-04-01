import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def get_rivals_news():
    # Căutăm mai multe variante ca să găsim sigur ceva nou acum
    queries = [
        "Roblox Rivals update news", 
        "Roblox Rivals codes", 
        "Roblox Rivals game news"
    ]
    
    new_articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for query in queries:
        # Adresa corectă pentru Google News RSS
        rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
        try:
            response = requests.get(rss_url, headers=headers, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                # Luăm cele mai noi 3 rezultate din fiecare căutare
                for item in root.findall('.//item')[:3]:
                    title = item.find('title').text
                    link = item.find('link').text
                    
                    # Verificăm să nu adăugăm aceeași știre de două ori în lista temporară
                    if title not in [a['title'] for a in new_articles]:
                        new_articles.append({
                            "title": title,
                            "link": link,
                            "date": datetime.now().strftime("%Y-%m-%d")
                        })
        except Exception as e:
            print(f"Search error for {query}: {e}")
            continue
    return new_articles

def update_archive():
    # ȘTIRI FIXE - Baza ta de date de la început
    static_news =     # ȘTIRI FIXE - Doar Mesaje Text (fără link-uri externe)
    static_news = [
        {"title": "🔥 NEW CODES! Use '100MVISITS' for a Free Rare Crate and 5,000 Coins! 💰", "date": "2026-04-01"},
        {"title": "🚀 CYBER UPDATE: New 'Neon City' Map is now LIVE! Optimized for 1v1 Snipers! 🏙️⚡", "date": "2026-03-28"},
        {"title": "🏆 SEASON 5 RESET: The Global Leaderboards are OPEN! Can you reach Top 100? ✨", "date": "2026-03-25"},
        {"title": "🔫 NEW BUNDLE: Get the 'Inferno Dragon' Sniper Skin! Limited time only! 🐉🔥", "date": "2026-03-20"},
        {"title": "⚙️ PERFORMANCE PATCH: Fixed lag spikes and improved hit registration! 🛠️✅", "date": "2026-03-15"}
    ]


    # 1. Verificăm dacă există deja arhiva
    if os.path.exists('news.json'):
        try:
            with open('news.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                archive = data.get("articles", [])
        except:
            archive = static_news.copy()
    else:
        archive = static_news.copy()

    # 2. Luăm noutățile noi
    fresh_news = get_rivals_news()
    
    # 3. Adăugăm doar noutățile care NU sunt deja în arhivă
    existing_titles = {art['title'] for art in archive}
    added_count = 0
    
    for news in fresh_news:
        if news['title'] not in existing_titles:
            archive.insert(0, news) # Cele noi apar primele
            added_count += 1

    # 4. Limităm arhiva la 25 de postări
    archive = archive[:25]

    # 5. Salvăm fișierul final
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles": archive
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Success! Added {added_count} new items.")

if __name__ == "__main__":
    update_archive()
