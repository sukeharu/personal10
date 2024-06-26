import requests
from bs4 import BeautifulSoup

url = 'https://www.mof.go.jp/jgbs/individual/kojinmuke/'
res = requests.get(url, timeout=5)
res.encoding = 'shift_jis'
res.raise_for_status()

# 画像のパスを取得
soup = BeautifulSoup(res.text, 'html.parser')
picture = soup.find(class_="home-rate-description").picture
picture_children = picture.children
for child in picture_children:
    if child.name == 'source' and child['media'] == '(min-width:768px)':
        print(child['srcset'])
