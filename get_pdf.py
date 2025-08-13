import requests
from bs4 import BeautifulSoup
import pdfplumber
from io import BytesIO



# base_url = "https://cse.ttu.edu.tw"
# latest_news_url = "https://cse.ttu.edu.tw/p/406-1058-38942,r61.php"

# res = requests.get(latest_news_url)
# res.raise_for_status()  # 確保請求成功
# soup = BeautifulSoup(res.text, 'html.parser')

# for data in soup.find_all(class_='minner'):
#     a_tag = data.find('a')
#     if not a_tag:
#         continue
    
#     link = a_tag.get('href')
#     full_link = link if link.startswith('http') else base_url + link

#     if full_link.endswith('.pdf'):
#         print(full_link)
#         url = full_link
#         response = requests.get(url)
#         # 用 BytesIO 包裝成檔案物件
#         pdf_file = BytesIO(response.content)

#         with pdfplumber.open(pdf_file) as pdf:
#             text = ""
#             for page in pdf.pages:
#                 text += page.extract_text() + "\n"
        
        # print(f"連結: {full_link}")
        # print(f"pdf內文:{text}")
        # print('\n')

def extract_text_from_pdf(pdf_url):
    base_url = "https://cse.ttu.edu.tw"
    res = requests.get(pdf_url)
    res.raise_for_status()  # 確保請求成功
    soup = BeautifulSoup(res.text, 'html.parser')

    for data in soup.find_all(class_='minner'):
        a_tag = data.find('a')
        if not a_tag:
            continue
        
        link = a_tag.get('href')
        full_link = link if link.startswith('http') else base_url + link

        if full_link.endswith('.pdf'):
            url = full_link
            response = requests.get(url)
            # 用 BytesIO 包裝成檔案物件
            pdf_file = BytesIO(response.content)

            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            
            return(text)

# print(extract_text_from_pdf("https://cse.ttu.edu.tw/p/406-1058-38575,r61.php"))
