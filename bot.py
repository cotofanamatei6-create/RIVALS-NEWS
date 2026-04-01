import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_rivals_news():
    # Căutăm mai multe variante ca să fim siguri că găsim ceva
    queries = [
        "Roblox Rivals update", 
        "Roblox Rivals codes", 
        "Roblox Rivals news",
        "Rivals Roblox game"
    ]
    
    new_articles = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for query in queries:
        rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
        try:
            response = requests.get(rss_url, headers=headers, timeout=10)
            root = ET.fromstring(response.content)
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                link = item.find('link').text
                # Curățăm titlul de numele site-ului care apare la final după " - "
                clean_title = title.split(' - ')[0]
                
                new_articles.append({
                    "title": clean_title,
                    "link": link,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        except:
            continue
    return new_articles

def update_archive():
    # 1. Citim ce avem deja (Arhiva)
    try:
        with open('news.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            archive = data.get("articles", [])
    except:
        archive = []

    # 2. Luăm noutățile
    fresh_news = get_rivals_news()
    
    # 3. Adăugăm doar ce e nou și UNIC
    existing_titles = {art['title'] for art in archive}
    added_count = 0
    
    for news in fresh_news:
        if news['title'] not in existing_titles:
            archive.insert(0, news)
            added_count += 1

    # Dacă arhiva e goală de tot, punem un mesaj de test să fim siguri că merge site-ul
    if not archive:
        archive.append({
            "title": "System Active: Waiting for new Roblox Rivals updates...",
            "link": "https://roblox.com",
            "date": datetime.now().strftime("%Y-%m-%d")
        })

    # 4. Salvăm (maxim 30 de știri)
    output = {
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "articles": archive[:30]
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Added {added_count} items.")

if __name__ == "__main__":
    update_archive()
