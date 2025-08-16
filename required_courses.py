import requests
from bs4 import BeautifulSoup
from get_pdf import extract_text_from_pdf 
import sqlite3
import os

#定義資料庫位置
db_path = os.path.join(os.getcwd(), "cs.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# c.execute("""
# CREATE TABLE IF NOT EXISTS "required_courses" (
    # tontent TEXT
# )
# """)
# conn.commit()

required_courses_url = "https://cse.ttu.edu.tw/p/412-1058-2032.php"
# print(required_courses_url)
res = requests.get(required_courses_url)
soup = BeautifulSoup(res.text, 'html.parser')

for link in soup.find_all('a', href=True):
    if "大學部學生必修科目表" in link.text:
        pdf_url = "https://cse.ttu.edu.tw" + link['href']

        print("PDF 路徑：", pdf_url)
        print("標題：", link.get('title'))
        break
print(extract_text_from_pdf(pdf_url))

db_path = os.path.join(os.getcwd(), "cs.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS required_courses")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS required_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        標題 TEXT NOT NULL UNIQUE,
        內文 TEXT NOT NULL
    )
""")
conn.commit()

# 寫入資料庫
try:
    cursor.execute("""
        INSERT OR REPLACE INTO required_courses (標題, 內文)
        VALUES (?, ?)
    """, (link.get('title'), extract_text_from_pdf(pdf_url)))
    conn.commit()
except sqlite3.Error as e:
    print(f"寫入資料庫失敗 ({link.get('title')}): {e}")
