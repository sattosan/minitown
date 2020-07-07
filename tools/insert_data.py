import json
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()

categories = ["men", "women"]

for category in categories:
    file_name = f"{category}_{os.environ['BASE_FILE_NAME']}"

    # ファイル読み込み
    with open(file_name, 'r') as f:
        # json形式に変換
        rakuten_fashions = json.load(f)

    # Elasticsearchインスタンスを作成
    es = Elasticsearch("http://elasticsearch:9200")

    # ファッションデータをElasticsearchにインポート
    for rakuten_fashion in rakuten_fashions:
        # ファッションデータ
        rakuten_fashion_item = rakuten_fashion['Item']
        # 性別の追加
        rakuten_fashion_item["sex"] = category
        try:
            # ドキュメントの作成
            es.create(index='fashion',
                      id=rakuten_fashion_item['itemCode'],
                      body=rakuten_fashion_item)
            print(f"{rakuten_fashion_item['itemName'][1:30]}... created")

        except Exception:
            pass
