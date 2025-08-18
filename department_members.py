import requests
from bs4 import BeautifulSoup
import sqlite3
import os

def main():
    # 定義資料庫位置
    db_path = os.path.join(os.getcwd(), "cs.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS department_members")
    c.execute("""
        CREATE TABLE IF NOT EXISTS department_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            人物 TEXT NOT NULL UNIQUE,
            電話 TEXT NOT NULL,
            信箱 TEXT NOT NULL,
            辦公室 TEXT NOT NULL,
            metadata TEXT NOT NULL
        )
    """)
    conn.commit()
    speech_announcement_url = "https://cse.ttu.edu.tw/p/412-1058-157.php?Lang=zh-tw"

    res = requests.get(speech_announcement_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    seen = set()
    all_info = []
    
    for mdetail in soup.find_all(class_="mdetail"):
        all_info = []
        # print(mdetail.get_text(strip=True))
        name = mdetail.find_all(style="color:#0000cd;")
        n = ', '.join([x.get_text(strip=True) for x in name if x.get_text(strip=True)])
        if n:
            all_info.append(n)
        # print(n)
        
        info = mdetail.find_all('p')
        # print(info)
        for add in info:
            add_str = add.get_text(strip=True)
            
            # 預設沒找到重複
            trash = False
            
            for x in all_info:
                if add_str in x or add_str == '學術研究發表｜研究計畫':
                    trash = True
                    break  # 找到重複就跳出
            if not trash:
                all_info.append(add_str)
        
        if '兼任' in all_info[0]:
            print("人物:", all_info[0])
            for text in all_info:
                if 'E-mail' in text:
                    print("信箱:"+text)
            combined_string = "。".join(all_info[1:3])
            print("metadata: " + combined_string)
            print('-'*20)
            try:
                c.execute("""
                    INSERT OR REPLACE INTO department_members (人物, 電話, 信箱, 辦公室, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (all_info[0], '', all_info[4], '', combined_string))
                conn.commit()
            except sqlite3.Error as e:
                print(f"寫入資料庫失敗 : {e}")
                print()
            continue

        print("人物:" + all_info[0])
        print("電話:" + all_info[1])
        print("信箱:" + all_info[2])
        print("辦公室:" + all_info[3])
        combined_string = "".join(all_info[4:])  # 把從第4個開始的字串合併
        print("metadata: " + combined_string)

        print('-'*20)
        
        try:
            c.execute("""
                INSERT OR REPLACE INTO department_members (人物, 電話, 信箱, 辦公室, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (all_info[0], all_info[1], all_info[2], all_info[3], combined_string))
            conn.commit()
        except sqlite3.Error as e:
            print(f"寫入資料庫失敗 : {e}")
            print()

    conn.close()
        
if __name__ == "__main__":
    main()