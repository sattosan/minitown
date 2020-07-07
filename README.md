# MINITOWN
某ファッションサイトの検索機能をElasticsearchを使ってシンプルに実装したサービスになります．

## DEMO
準備中...

## Features
- フリーワード検索
- 価格を指定した検索
- 性別を指定した検索

## Requirement
Docker及びDocker Composeがインストールされていることを前提としています．

```bash
# Docker Version
$ docker -v
Docker version 19.03.12, build 48a66213fe
```


```bash
# Docker Compose
$ docker-compose -v
docker-compose version 1.26.0, build d4451659
```

## Installation

### 準備
```bash
$ git clone https://github.com/sattosan/minitown.git

$ cd minitown
```

### コンテナの作成と起動
```bash
$ docker-compose up -d --build
```

### ファッションデータをAPIから取得し作成する
```bash
$ docker-compose run --rm tools python create_datafile.py
```

### 取得したデータをElasticsearchにインポートする
```bash
$ docker-compose run --rm tools python insert_data.py
```

## Usage
準備中...

## Note
