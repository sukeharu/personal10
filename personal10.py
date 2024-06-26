#! /usr/bin/env python3


import argparse
from io import BytesIO
from PIL import Image
import pytesseract # https://pypi.org/project/pytesseract/
import regex as re
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup


def get_image_url() -> str:
    """get_image()
    財務省個人向け国債サイトから対象の画像を取得する


    """
    url = 'https://www.mof.go.jp/jgbs/individual/kojinmuke/'
    res = requests.get(url, timeout=5)
    res.encoding = 'shift_jis'
    res.raise_for_status()

    # 画像のパスを取得
    soup = BeautifulSoup(res.text, 'html.parser')
    picture_children = soup.find(class_="home-rate-description").picture
    for child in picture_children:
        if child.name == 'source' and child['media'] == '(min-width:768px)':
            imgurl = child['srcset']

    return urljoin(url, imgurl)


def scan_image(url: str, test=''):
    """scan_image()
    画像をOCRにかけてテキストを取得

    Parameters
    ----------
    url:
        スキャンする画像のURL

    Returns
    -------
    str:
        スキャンした結果（テキスト）
    """

    if not test:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        img = Image.open(BytesIO(res.content))
    else:
        img = Image.open(test)


    return pytesseract.image_to_string(img, lang='jpn')


def main(args):
    """personal10
    10年もの個人向け国債の利率をチェック。
    とりあえずはpytesseractを試しに使ってみる

    Parameters
    ----------
    args : ArgumentParser
        ArgumentParser object.

    Returns
    -------
    None
    """

    # 画像のテキストを取得
    if localpath := args.test:
        text = scan_image('./rate-051.jpg', test=localpath)
    else:
        text = scan_image(get_image_url())
        # print(text)

    if re.search(r'現在募集は行っておりません', text):
        # 募集中かどうかをチェック
        print('個人向け国債10年もの : 現在募集していない')
    else:
        # 募集中の場合利率を表示
        if (result := re.search(r'^(\d+\.\d+)', text, flags=re.MULTILINE)):
            print(f'個人向け国債10年もの : 募集中 初回利率{result.group(1)}%')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="個人向け国債10年もの利率をチェック"
    )
    parser.add_argument(
        "-t",
        "--test",
        help="テストモード。オフラインの画像をスキャンできる。パスを指定すること。",
        type=str,
        default=''
    )
    main(parser.parse_args())
