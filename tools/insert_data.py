import json
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
load_dotenv()


with open(os.environ["FILE_NAME"], 'r') as f:
    rakuten_fashions = json.load(f)

es = Elasticsearch("http://elasticsearch:9200")

for rakuten_fashion in rakuten_fashions:
    rakuten_fashion_item = rakuten_fashion['Item']
    try:
        es.create(index='fashion',
                  id=rakuten_fashion_item['itemCode'],
                  body=rakuten_fashion_item)
    except Exception:
        pass
    print(f"{rakuten_fashion_item['itemName'][1:30]}... created")
