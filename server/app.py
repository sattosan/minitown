from flask import Flask, request, url_for, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_results():
    es = Elasticsearch('http://elasticsearch:9200')

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

    if (search_word := request.form.get('search_word')):
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

    if (price_min := request.form.get('price_min')):
        body['query']['bool']['must'].append(
            {"range": {"itemPrice": {"gte": price_min}}})

    if (price_max := request.form.get('price_max')):
        body['query']['bool']['must'].append(
            {"range": {"itemPrice": {"lte": price_max}}})

    result = es.search(index='fashion', body=body, size=50)
    result_num = result['hits']['total']['value']
    fashions = result['hits']['hits']

    return render_template('index.html',
                           result_num=result_num,
                           fashions=fashions,
                           request_form=request.form)

# ブラウザキャッシュ無効
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# サーバ起動
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
