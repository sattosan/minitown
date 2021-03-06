from elasticsearch import Elasticsearch


# Elasticsearchを使って検索
def search(param):
    # Elasticsearchインスタンスを作成
    es = Elasticsearch("http://elasticsearch:9200")

    # Elasticsearchに投げるクエリ
    body = {
        "query": {
            "bool": {
                "must": []
            }
        },
        "highlight": {
            "fields": {
                "itemName": {},
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

    # 性別が選択された場合
    if (sex := param.get('sex')) and not sex == "all":
        body['query']['bool']['must'].append(
            {'term': {'sex': {'value': sex}}}
        )

    # Elasticsearchにクエリを投げて商品を検索
    result = es.search(index='fashion', body=body, size=100)

    return result


# ドキュメントから必要なファション情報を抽出
def trim_fashions(documents):
    fashions = []

    for document in documents:
        name = document["_source"]["itemName"]
        shop_name = document["_source"]["shopName"]
        price = document["_source"]["itemPrice"]
        caption = document["_source"]["itemCaption"]

        # 画像がなければ
        if len(document["_source"]["mediumImageUrls"]) == 0:
            continue
        else:
            image_url = document["_source"]["mediumImageUrls"][0]["imageUrl"]

        if "highlight" in document:
            # ハイライトにitemCaptionがあれば
            if "itemCaption" in document["highlight"]:
                caption = document["highlight"]["itemCaption"][0]
            # ハイライトにitemCaptionがなかった場合itemNameをハイライト
            elif "itemName" in document["highlight"]:
                name = document["highlight"]["itemName"][0]

        fashions.append({
            "name": name,
            "image_url": image_url,
            "shop_name": shop_name,
            "price": price,
            "caption": caption
        })

    return fashions
