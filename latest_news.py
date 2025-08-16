import requests
from bs4 import BeautifulSoup
from get_pdf import extract_text_from_pdf
import sqlite3
import os

def fetch_pdf_link(news_url):#輸入最新消息的網址 取得pdf的連接 呼叫extract_text_from_pdf
    """從新聞頁面中抓取全部的PDF連結"""
    base_url = "https://cse.ttu.edu.tw"
    res = requests.get(news_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    pdf_links = []
    # 尋找所有 <a>，並找出 href 包含 .pdf 的
    for data in soup.find_all(class_='mptattach'):
        # print(data)
        for a_tag in data.find_all('a'):
            href = a_tag.get('href')
            if href:
                pdf_links.append(base_url + href)
    return pdf_links

def main():
    latest_news_url = "https://cse.ttu.edu.tw/p/403-1058-61-1.php?Lang=zh-tw"

    # 建立新的資料庫連接
    db_path = os.path.join(os.getcwd(), "cs.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS latest_news")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS latest_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            標題 TEXT NOT NULL UNIQUE,
            連結 TEXT NOT NULL,
            發布時間 TEXT NOT NULL,
            內文 TEXT NOT NULL,
            pdf內容 TEXT
        )
    """)
    conn.commit()
    res = requests.get(latest_news_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    for data in soup.find_all(class_="mtitle"):
        a_tag = data.find('a')
        title = a_tag.get_text(strip=True) if a_tag else ''
        link = a_tag['href'] if a_tag and a_tag.has_attr('href') else ''
        publish_time_tag = data.find('i', class_='mdate after')
        publish_time = publish_time_tag.get_text(strip=True) if publish_time_tag else ''

        res_content = requests.get(link)
        soup_content = BeautifulSoup(res_content.text, 'html.parser')
        content = "\n".join([item.get_text(strip=True) for item in soup_content.find_all(class_='mpgdetail')])
        pdf_link= fetch_pdf_link(link)
        pdf_text = extract_text_from_pdf(pdf_link)

        # 寫入資料庫
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO latest_news (標題, 連結, 發布時間, 內文, pdf內容)
                VALUES (?, ?, ?, ?, ?)
            """, (title, link, publish_time, content, pdf_text))
            conn.commit()
        except sqlite3.Error as e:
            print(f"寫入資料庫失敗 ({title}): {e}")

        print("Title:", title)
        print("Link:", link)
        print("Published:", publish_time)
        print("Content :",content)
        print("PDF link:", pdf_link if pdf_link else "")
        # print("PDF content:", pdf_text if pdf_text else "")
        print("-" * 40)
    conn.close()
if __name__ == "__main__":
    main()
