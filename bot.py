import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_rivals_news():
    # Searching for Roblox Rivals specific updates and news
    query = "Roblox Rivals game update news"
    rss_url = f"https://google.com{query}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        
        news_items = []
        # Get the latest 5 news items
        for item in root.findall('.//item')[:5]: 
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            
            news_items.append({
                "title": title,
                "link": link,
                "date": pub_date
            })
        return news_items
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def update_site_data():
    news = get_rivals_news()
    data = {
        "last_update": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "articles": news
    }
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("News successfully updated in English!")

if __name__ == "__main__":
    update_site_data()
