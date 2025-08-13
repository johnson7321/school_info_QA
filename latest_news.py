import requests
from bs4 import BeautifulSoup
from get_pdf import extract_text_from_pdf 
import sqlite3
import os

#定義資料庫位置
# db_path = os.path.expanduser('~/cs.db')
db_path = r"C:\Users\User\Desktop\crawl_cs\cs.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS "latest news" (
    "標題" TEXT NOT NULL UNIQUE,
    "連結" TEXT NOT NULL,
    "發布時間" TEXT NOT NULL,
    "內文" TEXT NOT NULL,
    "pdf內容" TEXT,
    PRIMARY KEY("標題")
)
""")
conn.commit()

base_url = "https://cse.ttu.edu.tw/"  # 網站主域名
latest_news_path = "/p/403-1058-61-1.php"
latest_news_url = base_url + latest_news_path
import sqlite3

res = requests.get(latest_news_url)
soup = BeautifulSoup(res.text, 'html.parser')
# print(res.text)

for data in soup.find_all(class_='mtitle'):
    a_tag = data.find('a')
    time_tag = data.find('i', class_='mdate after')
    
    text = a_tag.get_text(strip=True) if a_tag else ''
    link = a_tag.get('href') if a_tag else ''
    time_text = time_tag.get_text(strip=True) if time_tag else ''

    res =   requests.get(link)
    content_soup = BeautifulSoup(res.text, 'html.parser')
    # content = [data.get_text(strip=True) for data in content_soup.find_all(class_='mpgdetail')]
    content_list = [item.get_text(strip=True) for item in content_soup.find_all(class_='mpgdetail')]
    content = "\n".join(content_list)  # 把 list 轉成字串
    
    c.execute("""
        INSERT OR REPLACE INTO "latest news" (標題, 連結, 發布時間, 內文, pdf內容)
        VALUES (?, ?, ?, ?, ?)
    """, (text, link, time_text, content, extract_text_from_pdf(link)))

    conn.commit()

    print(f"標題: {text}")
    print(f"內文連結: {link}")
    print(f"發布時間: {time_text}")
    print(f"內文: {content}")
    print(f"PDF 內容: {extract_text_from_pdf(link)}")
    print('\n')
