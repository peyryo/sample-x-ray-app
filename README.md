# AWS X-Ray サンプルアプリ

X-Ray を動かすサンプルアプリケーションです．

## 環境

- python 3.8.5
- aws-cli/1.16.233

## ディレクトリ構成

```text
sample-x-ray-app
│  .gitignore
│  README.md
│  template.yml <-- CloudFormation のテンプレート
│
└─src <-- Lambda 関数のソースファイル
    └─PostFunction
            lambda_handler.py
            requirements.txt
```

## デプロイ手順

デプロイに必要なS3バケットは事前に作成しておく必要があります．
作成したバケット名を，`<YOUR S3 BUCKET NAME>` と置き換えてコマンドを実行してください．

```bash
# lambda に必要なパッケージのインストール
pip install -r src/PostFunction/requirements.txt -t src/PostFunction/

# lambda のデプロイ
aws cloudformation package \
    --template-file template.yml \
    --s3-bucket <YOUR S3 BUCKET NAME> \
    --output-template-file packaged-template.yml

aws cloudformation deploy \
    --template-file packaged-template.yml \
    --stack-name <YOUR S3 BUCKET NAME> \
    --capabilities CAPABILITY_NAMED_IAM
```
