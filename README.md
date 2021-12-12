# Automate connpass appointment posting. 

Automatically register reservation post emails for delivery URLs and survey URLs for online study sessions on connpass.

## パッケージのインストール

```shell
pip3 install selenium
# ドライバーはChomeのバージョンと併せてインストールすること
pip3 install chromedriver-binary==??.?.????.?.??
```

## 環境設定

設定情報は  ~/config.ini ファイルに格納する必要があります。
ご自身のconnpassのユーザー/パスワード、コミュニティ名、イベントの各種情報をエディタを使ってを編集してください。

## 実行方法

```shell
$ python main.py
```

詳細はこちらを参照
