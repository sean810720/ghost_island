'''
Author: Sean
Date: 2021-05-23 01:44:57
LastEditTime: 2021-05-25 10:29:51
Description: Crawler of Taiwan water (水庫剩餘量)
'''

import requests
import json
from bs4 import BeautifulSoup

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
    doc_ref = db.reference('water')
    data = []

    # 台灣水庫即時水情

    # 水情數據
    res0 = requests.get(
        "https://www.taiwanstat.com/waters/latest", verify=False)
    res0.encoding = 'utf8'
    json = json.loads(res0.text)

    # 水情介面
    res = requests.get(
        "https://water.taiwanstat.com", verify=False)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text, "html.parser")

    # 整理資料
    for item in soup.select(".reservoir .name h3"):

        # 水庫名稱
        name = item.text
        key = item.text.split("(")[0]
        print("\n水庫名稱:", name)

        # 有效蓄水量
        volumn = json[0][key]["volumn"]
        print("總蓄水量(立方公尺):", volumn)

        # 剩餘水量
        percentage = json[0][key]["percentage"]
        print("剩餘水量(%):", percentage)

        # 剩餘天數計算

        # 剩餘量
        remain_available = float(
            json[0][key]["baseAvailable"]) * float(percentage) / 100

        # 淨使用量
        daliy_net_flow = "---" if json[0][key]["daliyNetflow"] == "--" or json[0][key]["daliyNetflow"] <= 0 else float(
            json[0][key]["daliyNetflow"])

        # 剩餘天數
        due_day = "---" if daliy_net_flow == "---" else int(
            remain_available / daliy_net_flow)
        print("剩餘天數:", due_day)

        # 水量狀態
        remain_available_status = "上升" if json[0][key]["daliyNetflow"] != "--" and json[0][key][
            "daliyNetflow"] <= 0 else "下降"
        print("水量狀態:", remain_available_status)

        # 更新時間
        update_at = json[0][key]["updateAt"]
        print("更新時間:", update_at)

        data.append({
            "name": name,
            "volumn": volumn,
            "percentage": percentage,
            "due_day": due_day,
            "remain_available_status": remain_available_status,
            "update_at": update_at
        })

    # 寫入 database reference.
    doc_ref.set(data)
    print("\nTaiwan water updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan water updated")
