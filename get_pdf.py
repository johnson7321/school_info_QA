import requests
from bs4 import BeautifulSoup
import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_links):
    # 強制嘗試下載並解析 PDF，不以副檔名判斷
    pdf_content = []
    for full_link in pdf_links if isinstance(pdf_links, list) else [pdf_links]: 
        try:
            response = requests.get(full_link)
            response.raise_for_status()
        except Exception as e:
            print(f"下載 PDF 失敗: {e}")
            return None

        pdf_file = BytesIO(response.content)

        try:
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text 
                pdf_content.append(text.strip())
        except Exception as e:
            print(f"解析 PDF 失敗: {e}")
            return None
    text = '\n'.join(pdf_content) if pdf_content else ''  # 空的 list 也會變成空字串
    return text

# 測試用，請換成真正的 PDF 連結
# test = ['https://cse.ttu.edu.tw/var/file/58/1058/attach/34/pta_35925_9531610_47618.pdf', 'https://cse.ttu.edu.tw/var/file/58/1058/attach/34/pta_35926_9910150_47618.pdf']
# for content in extract_text_from_pdf(test):
#     print(content)