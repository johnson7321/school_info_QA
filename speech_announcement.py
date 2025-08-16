import requests
from bs4 import BeautifulSoup
import sqlite3
import os

def main():
    #定義資料庫位置
    db_path = os.path.join(os.getcwd(), "cs.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS speech_announcement")
    c.execute("""
        CREATE TABLE IF NOT EXISTS speech_announcement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            標題 TEXT NOT NULL UNIQUE,
            講師 TEXT NOT NULL,
            時間 TEXT NOT NULL,
            地點 TEXT NOT NULL
        )
    """)
    conn.commit()
    speech_announcement_url = "https://cse.ttu.edu.tw/p/403-1058-111-1.php"

    res = requests.get(speech_announcement_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    for link in soup.find_all(class_="mtitle"):
        a_tag = link.find('a')
        speech_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else ''
        
        res = requests.get(speech_url)
        soup = BeautifulSoup(res.text, 'html.parser')
            
        # 1. 取得標題（日期 + 講座主題）
        title = soup.find('h2', class_='hdline').text.strip()
        print('標題:', title)

        # 2. 取得 meditor 裡面的資訊
        meditor_div = soup.find('div', class_='mpgdetail')

        # meditor_div 內的文本用 <br/> 斷行，可以用 .stripped_strings 把每行整理成 list
        lines = list(meditor_div.stripped_strings)
        
        # 如果想把講師、時間、地點單獨取出來，可以做簡單字串切割
        info = {}
        for line in lines:
            if ':' in line:
                key, val = line.split(':', 1)
                info[key.strip()] = val.strip()

        print('講師:', info.get('講師'))
        print('時間:', info.get('時間'))
        print('地點:', info.get('地點'))
        print("-" * 40)

        # 寫入資料庫
        try:
            c.execute("""
                INSERT OR REPLACE INTO speech_announcement (標題, 講師, 時間, 地點)
                VALUES (?, ?, ?, ?)
            """, (title, info.get('講師'), info.get('時間'), info.get('地點')))
            conn.commit()
        except sqlite3.Error as e:
            print(f"寫入資料庫失敗 ({title}): {e}")

    conn.close()

if __name__ == "__main__":
    main()