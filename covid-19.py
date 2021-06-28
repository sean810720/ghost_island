'''
Author: Sean
Date: 2021-05-22 23:21:42
LastEditTime: 2021-06-28 18:00:38
Description: Crawler of Taiwan Covid-19 statistics (台灣疫情報告)
'''

import requests
from bs4 import BeautifulSoup
import time

# 初始化 Firebase 連接
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate(
    "./Firebase/ghost-island-ab1d8-firebase-adminsdk-swrsg-a2201ff4d7.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://ghost-island-ab1d8-default-rtdb.firebaseio.com/'})

try:

    # Get a database reference.
    doc_ref = db.reference('covid-19')
    data = []

    # 台灣疫情報告
    res = requests.get(
        "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php", verify=False)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text, "html.parser")

    # 累積確診
    total_confirmed = "0" if len(soup.select(
        ".country_confirmed")) == 0 else soup.select(".country_confirmed")[0].text
    print("累積確診:", total_confirmed)

    # 累積死亡
    total_deaths = "0" if len(soup.select(
        ".country_deaths")) == 0 else soup.select(".country_deaths")[0].text
    print("累積死亡:", total_deaths)

    # 病死率
    rate_deaths = "0%" if len(soup.select(
        "#country_cfr")) == 0 else soup.select("#country_cfr")[0].text
    print("病死率:", rate_deaths)

    # 新增確診
    new_confirmed = "0" if len(soup.select(
        ".country_recovered")) == 0 else soup.select(".country_recovered")[0].text.split("+")[1]
    print("新增確診:", new_confirmed)

    # 新增死亡
    new_deaths = "0" if len(soup.select(
        ".country_deaths_change")) == 0 else soup.select(".country_deaths_change")[0].text
    if len(new_deaths.strip()) == 0:
        new_deaths = "0"
    else:
        new_deaths = new_deaths.split("+")[1]
    print("新增死亡:", new_deaths)

    data.append({
        "total_confirmed": total_confirmed,
        "total_deaths": total_deaths,
        "rate_deaths": rate_deaths,
        "new_confirmed": new_confirmed,
        "new_deaths": new_deaths,
        "record_date": time.strftime("%Y年%m月%d日", time.localtime())
    })

    # 寫入 database reference.
    doc_ref.set(data)
    print("\nTaiwan Covid-19 statistics updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan Covid-19 statistics updated")
