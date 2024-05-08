import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# 最初にアクセスするURL
start_url = 'https://zdh.stagingbridge.net/'

visited_urls = set()
urls_to_visit = {start_url}
aws_articles = []

# 配下のURLも含めるためループ処理開始
while urls_to_visit:
    current_url = urls_to_visit.pop()
    print(f"Visiting: {current_url}")
    try:
        response = requests.get(current_url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # AWSというテキストを含む部分を検索
        if 'AWS' in soup.get_text():
            title = soup.find('title').get_text(strip=True) if soup.find('title') else 'No Title'
            print(f"Found AWS in: {current_url} - {title}")
            aws_articles.append([title, current_url])

        # このページのリンクを見つけて、まだ訪れていないものを追加
        # 関係ないページを除くためhttps://zdh.～から始まるURLのみを対象にします。
        for link in soup.find_all('a', href=True):
            absolute_link = urljoin(current_url, link['href'])
            if absolute_link.startswith('https://zdh.') and absolute_link not in visited_urls:
                urls_to_visit.add(absolute_link)

        visited_urls.add(current_url)
    except Exception as e:
        print(f"Error visiting {current_url}: {e}")

    # 重複を避けるため、訪れたURLをリストから削除
    urls_to_visit -= visited_urls

    # 無限ループにならないように、訪問するURLの数を制限
    if len(visited_urls) > 100:
        break

# CSVファイルに結果を保存するパス
csv_file_path = r'C:\Users\hiroko.takeda\OneDrive - 株式会社アバント\ドキュメント\技術支援勉強会\aws_articles.csv'

with open(csv_file_path, 'w', newline='', encoding='shift_jis') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'URL'])  # ヘッダー
    writer.writerows(aws_articles)

print(f'Found {len(aws_articles)} articles related to AWS. Data has been saved to "{csv_file_path}"')