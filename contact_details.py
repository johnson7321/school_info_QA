import requests
from bs4 import BeautifulSoup
import sqlite3
import os

def main():
    # 定義資料庫位置
    db_path = os.path.join(os.getcwd(), "cs.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS contact_details")
    c.execute("""
        CREATE TABLE IF NOT EXISTS contact_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            項目 TEXT NOT NULL UNIQUE,
            承辦人 TEXT NOT NULL,
            分機 TEXT NOT NULL
        )
    """)
    conn.commit()
    speech_announcement_url = "https://recruit.ttu.edu.tw/p/412-1068-2684.php?Lang=zh-tw#start-C"

    res = requests.get(speech_announcement_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_text1 = []
    all_text2 = []
    
    for table in soup.find_all("table"):
        data = table.find_all('th',string = '項目') 
        if data:
            td = table.find_all('td')
            if td:
                for text in td:
                    # print(text.get_text(strip=True))
                    all_text1.append(text.get_text(strip=True))
                    # print("-" * 40)

        data = table.find_all('th',string = '業務項目')
        if data:
            td = table.find_all('td')
            if td:
                for text in td:
                    # print(text.get_text(strip=True))
                    all_text2.append(text.get_text(strip=True))
                    # print("-" * 40)

    for i in range(0, len(all_text1), 3):  # 步進3
        item = all_text1[i]            # 事項
        people = all_text1[i + 1]      # 負責人
        num = all_text1[i + 2]         # 電話
        print(f"事項: {item}, 負責人: {people},  聯絡電話: {num}")
        try:
            c.execute("""
                INSERT OR REPLACE INTO contact_details (項目, 承辦人, 分機)
                VALUES (?, ?, ?)
            """, (item, people, num))
            conn.commit()
        except sqlite3.Error as e:
            print(f"寫入資料庫失敗 ({item}): {e}")
            print()

    for i in range(0, len(all_text2), 3):  # 步進3
        people = all_text2[i]            
        item = all_text2[i + 1]      
        num = all_text2[i + 2]         # 電話
        print(f"事項: {item}, 負責人: {people},  聯絡電話: {num}")
        try:
            c.execute("""
                INSERT OR REPLACE INTO contact_details (項目, 承辦人, 分機)
                VALUES (?, ?, ?)
            """, (item, people, num))
            conn.commit()
        except sqlite3.Error as e:
            print(f"寫入資料庫失敗 ({item}): {e}")
            print()

    conn.close()
        
if __name__ == "__main__":
    main()