from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()


def search(param):
    # Elasticsearchクライアント
    es = Elasticsearch("http://elasticsearch:9200")

    # Elasticsearchに投げるクエリ
    body = {
        "query": {
            "bool": {
                "must": [
                ]
            }
        },
        "highlight": {
            "fields": {
                "itemCaption": {}
            }
        }
    }

    # キワードが入力された場合
    if (search_word := param.get('search_word')):
        body['query']['bool']['must'].append(
            {
                "bool": {
                    "should": [
                        {"match": {"itemName": search_word}},
                        {"match": {"itemCaption": search_word}}
                    ]
                }
            }
        )

    # 最低価格が入力された場合
    if (price_min := param.get('price_min')):
        body['query']['bool']['must'].append(
            {"range": {"itemPrice": {"gte": price_min}}})

    # 最高価格が入力された場合
    if (price_max := param.get('price_max')):
        body['query']['bool']['must'].append(
            {"range": {"itemPrice": {"lte": price_max}}})

    # Elasticsearchにクエリを投げて商品を検索
    result = es.search(index='fashion', body=body, size=50)

    return result
