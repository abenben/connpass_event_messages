import configparser
from datetime import datetime as dt
from datetime import timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By

import chromedriver_binary

# ----------------------------------------------------------
# 環境設定ファイルから情報取得
# ----------------------------------------------------------

cfg = configparser.ConfigParser()

# test.confから設定を読む
cfg.read("./config.ini", encoding='utf-8')

EVENT_DATE = dt.strptime(cfg["event"]["date"], '%Y/%m/%d')

# イベントURL
EVENT_URL = "https://connpass.com/event/{0}".format(cfg["event"]["connpass_id"])

# ----------------------------------------------------------
# イベントメッセージの投稿情報を編集する
# ----------------------------------------------------------

# メッセージのタイトル
DAY_BEFORE_NOTIFICATION_TITLE = "【 明日{start_time} 開始】{title} 配信URLのご連絡".format(
    start_time=cfg["event"]["start_time"],
    title=cfg["event"]["title"])
TODAY_NOTIFICATION_TITLE = "【 本日{start_time} 開始】{title} 配信URLのご連絡".format(
    start_time=cfg["event"]["start_time"],
    title=cfg["event"]["title"])
TODAY_SURVEY_TITLE = "【アンケートにご協力ください】{title}".format(
    title=cfg["event"]["title"])
DAY_AFTER_SURVEY_TITLE = "【アンケートにご協力ください】{title}（リマインダー）".format(
    title=cfg["event"]["title"])
TITLES = [DAY_BEFORE_NOTIFICATION_TITLE, TODAY_NOTIFICATION_TITLE, TODAY_SURVEY_TITLE, DAY_AFTER_SURVEY_TITLE]

# メッセージの本文
DAY_BEFORE_NOTIFICATION_MESSAGE = '''明日の配信先と質問サイトのURLをお知らせします。

イベント配信URL
　{date} {start_time}~
　{online_url}

発表者への質問はこちらのURLからお願いいたします。
　{question_url}
　(Slido.com #{question_id})

--
{community_name}'''.format(
    date=cfg["event"]["date"],
    start_time=cfg["event"]["start_time"],
    online_url=cfg["event"]["online_url"],
    question_url=cfg["event"]["question_url"],
    question_id=cfg["event"]["question_id"],
    community_name=cfg["community"]["name"])

TODAY_NOTIFICATION_MESSAGE = '''本日の配信先と質問サイトのURLをお知らせします。
（リマインダー）

イベント配信URL
　{date} {start_time}~
　{online_url}

発表者への質問はこちらのURLからお願いいたします。
　{question_url}
　(Slido.com #{question_id})

--
{community_name}'''.format(
    date=cfg["event"]["date"],
    start_time=cfg["event"]["start_time"],
    online_url=cfg["event"]["online_url"],
    question_url=cfg["event"]["question_url"],
    question_id=cfg["event"]["question_id"],
    community_name=cfg["community"]["name"])

TODAY_SURVEY_MESSAGE = '''皆様、本日はご視聴いただきありがとうございました。

今後の勉強会の満足度向上および登壇者へのフィードバックのためにアンケートを実施しております。

アンケートURL
　 {survey_url}

※所要時間：1,2分程度
※回答期限：{survey_deadline}

皆様の貴重なご意見、率直なご感想をお聞かせ下さい。

--
{community_name}'''.format(
    survey_url=cfg["event"]["survey_url"],
    survey_deadline=cfg["event"]["survey_deadline"],
    community_name=cfg["community"]["name"])

DAY_AFTER_SURVEY_MESSAGE = '''皆様、昨晩はご視聴いただきありがとうございました。
（リマインダー）

今後の勉強会の満足度向上および登壇者へのフィードバックのためにアンケートを実施しております。

アンケートURL
　 {survey_url}

※所要時間：1,2分程度
※回答期限：{survey_deadline}

皆様の貴重なご意見、率直なご感想をお聞かせ下さい。

--
{community_name}'''.format(
    survey_url=cfg["event"]["survey_url"],
    survey_deadline=cfg["event"]["survey_deadline"],
    community_name=cfg["community"]["name"])

MESSAGES = [DAY_BEFORE_NOTIFICATION_MESSAGE, TODAY_NOTIFICATION_MESSAGE, TODAY_SURVEY_MESSAGE, DAY_AFTER_SURVEY_MESSAGE]

# メッセージの投稿予約日
DATES = [EVENT_DATE - timedelta(1), EVENT_DATE, EVENT_DATE, EVENT_DATE + timedelta(1)]

# メッセージの投稿予約時間
TIMES = [cfg["event"]["notification_time"], cfg["event"]["notification_time"], cfg["event"]["survey_time"],
         cfg["event"]["re-survey_time"]]

# ----------------------------------------------------------
# 「参加者への情報」を編集する
# ----------------------------------------------------------

# connpassの「参加者への情報」へ登録する内容
event_box = '''【配信URL】
　{online_url}

【発表者への質問URL】
　{question_url}
　(Slido.com #{question_id})

【アンケートURL】
　 {survey_url}'''.format(
    online_url=cfg["event"]["online_url"],
    question_url=cfg["event"]["question_url"],
    question_id=cfg["event"]["question_id"],
    survey_url=cfg["event"]["survey_url"])

# ----------------------------------------------------------
# connpassサイトを操作して投稿予約、参加者への情報を編集する
# ----------------------------------------------------------

# ブラウザ起動
options = webdriver.chrome.options.Options()
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
driver = webdriver.Chrome(options=options)

# connpassログイン
driver.get("https://connpass.com/login/")
driver.find_element(By.NAME, "username").send_keys(cfg["connpass"]["username"])
driver.find_element(By.NAME, "password").send_keys(cfg["connpass"]["password"])
driver.find_element(By.CSS_SELECTOR, ".p > .btn").click()
driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td").click()

# イベントメッセージへの投稿予約
for title, message, date, time in zip(TITLES, MESSAGES, DATES, TIMES):
    driver.get(EVENT_URL + "/message/new/")
    driver.find_element(By.ID, "id_subject").send_keys(title)
    driver.find_element(By.NAME, "body").send_keys(message)
    driver.find_element(By.ID, "id_reserved_date").send_keys(date.strftime('%Y/%m/%d'))
    driver.find_element(By.ID, "id_reserved_time").send_keys(time)
    driver.find_element(By.ID, "id_send").click()

# connpassの「参加者への情報」に登録
driver.get(EVENT_URL)
driver.find_element(By.CSS_SELECTOR, ".icon_gray_edit").click()
driver.find_element(By.ID, "FieldParticipantOnlyInfo").click()
driver.find_element(By.NAME, "participant_only_info").clear()
driver.find_element(By.CSS_SELECTOR, ".save").click()
driver.find_element(By.ID, "FieldParticipantOnlyInfo").click()
driver.find_element(By.NAME, "participant_only_info").send_keys(event_box)
driver.find_element(By.CSS_SELECTOR, ".save").click()

# ブラウザを終了
driver.quit()
