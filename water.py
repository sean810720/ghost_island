'''
Author: Sean
Date: 2021-05-23 01:44:57
LastEditTime: 2021-05-24 11:49:05
Description: Crawler of Taiwan water (水庫剩餘量)
FilePath: /Crawler/water.py
'''

import requests
import json
from bs4 import BeautifulSoup

try:
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
        daliy_net_flow = float(
            json[0][key]["daliyNetflow"])

        # 剩餘天數
        due_day = int(remain_available / daliy_net_flow)
        due_day = 0 if due_day < 0 else due_day
        print("剩餘天數:", due_day)

        # 更新時間
        update_at = json[0][key]["updateAt"]
        print("更新時間:", update_at)

    print("\nTaiwan water updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan water updated")
