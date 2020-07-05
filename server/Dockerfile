FROM python:3.8-alpine

WORKDIR /usr/src/server

# コンテナ内で必要なパッケージをインストール
RUN apk add --no-cache build-base

COPY requirements.txt /tmp/
# requirements.txtにリストされたパッケージをインストールする
RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt

CMD flask run --debugger --reload --host 0.0.0.0 --port 5000