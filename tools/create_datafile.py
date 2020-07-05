import requests
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()

# API URL
URL = os.environ["RAKUTEN_URL"]

# クエリパラメータ
payload = {
    'format': 'json',
    'genreId': os.environ["MENS_CATEGORY_ID"],
    'applicationId': os.environ["APPLICATION_ID"],
    'page': 1
}

fashions = []

print("==========服の取得を開始==========")
while True:
    # 商品情報を取得
    response = requests.get(URL, params=payload)
    data = json.loads(response.text)
    print(f"{data['page']}ページ目取得")

    # 商品情報を配列に格納
    fashions.extend(data['Items'])
    # ページが最後だった場合ループを抜ける
    if data['pageCount'] == data['page']:
        break
    payload['page'] = data['page'] + 1

    # 楽天の制約より1秒遅延させる
    time.sleep(1)
print("==================完了==================")

print(f"====> {os.environ['FILE_NAME']}に書き込み")
with open(os.environ["FILE_NAME"], 'w') as f:
    # 日本語の文字化け対策しつつjson形式に変換
    json.dump(fashions, f, indent=2, ensure_ascii=False)
print("====> 書き込み完了")
