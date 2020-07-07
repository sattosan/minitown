import requests
import json
import time
import os
from dotenv import load_dotenv
load_dotenv()

# API URL
API_URL = os.environ["RAKUTEN_API"]

# ベースとなるクエリパラメータ
payload = {
    'format': 'json',
    'applicationId': os.environ["APPLICATION_ID"],
    'page': 1
}

# 性別に対応する楽天ジャンルID
categories = {
    "men": os.environ["MENS_CATEGORY_ID"],
    "women": os.environ["LADYS_CATEGORY_ID"]
}

for category, category_id in categories.items():
    # 初期化
    fashions = []
    payload['genreId'] = category_id
    payload['page'] = 1

    print(f"=========={category}服の取得を開始==========")
    while True:
        # 商品情報を取得
        response = requests.get(API_URL, params=payload)
        data = json.loads(response.text)
        print(f"{data['page']}/{data['pageCount']}ページ目を取得")

        # 商品情報を配列に格納
        fashions.extend(data['Items'])
        # ページが最後だった場合ループを抜ける
        if data['pageCount'] == data['page']:
            break
        payload['page'] = data['page'] + 1

        # 楽天の制約より1秒遅延させる
        time.sleep(1)
    print("==================完了==================")

    file_name = f"{category}_{os.environ['BASE_FILE_NAME']}"
    print(f"====> {file_name}に書き込み")
    with open(file_name, 'w') as f:
        # 日本語の文字化け対策しつつjson形式に変換
        json.dump(fashions, f, indent=2, ensure_ascii=False)
    print("====> 書き込み完了")
