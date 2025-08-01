import requests
from bs4 import BeautifulSoup

URL = 'https://www.mof.go.jp/jgbs/individual/kojinmuke/'
res = requests.get(URL, timeout=5)
res.encoding = 'shift_jis'
res.raise_for_status()

# 画像のパスを取得
soup = BeautifulSoup(res.text, 'html.parser')
picture = soup.find(class_="home-rate-img").picture
try:
    picture_children = picture.children
    for child in picture_children:
        if child.name == 'source' and child['media'] == '(min-width: 768px)':
            print(child['srcset'])
except AttributeError as e:
    print("Error: 要素が見つかりません。", e)
