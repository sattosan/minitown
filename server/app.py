from flask import Flask, request, url_for, render_template
from search import search

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_results():
    # 検索
    result = search(request.form)
    # ヒット件数
    result_num = result['hits']['total']['value']
    # 商品リスト
    fashions = result['hits']['hits']
    # ページのレンダリング
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
