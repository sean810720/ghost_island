'''
Author: Sean
Date: 2021-05-23 01:44:57
LastEditTime: 2021-05-24 15:25:33
Description: Crawler of Taiwan power (台電電力供應)
'''

import requests
import json

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
    doc_ref = db.reference('power')
    data = []

    # 台電電力供應
    res = requests.get(
        "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.json", verify=False)
    res.encoding = 'utf8'
    json = json.loads(res.text)

    # 目前用電量
    curr_load = json["records"][0]["curr_load"]
    print("目前用電量:", curr_load)

    # 目前使用率
    curr_util_rate = json["records"][0]["curr_util_rate"]
    print("目前使用率:", curr_util_rate)

    # 預估最高用電
    fore_peak_dema_load = json["records"][1]["fore_peak_dema_load"]
    print("預估最高用電:", fore_peak_dema_load)

    # 尖峰使用率
    fore_maxi_sply_capacity = json["records"][1]["fore_maxi_sply_capacity"]
    fore_peak_dema_load_rate = int(float(
        fore_peak_dema_load) / float(fore_maxi_sply_capacity) * 100)
    print("尖峰使用率:", fore_peak_dema_load_rate)

    # 預估最高用電時段
    fore_peak_hour_range = json["records"][1]["fore_peak_hour_range"]
    print("預估最高用電時段:", fore_peak_hour_range)

    # 最大供電能力
    print("預估最高用電:", fore_maxi_sply_capacity)

    # 備轉容量率
    fore_peak_resv_rate = float(json["records"][1]["fore_peak_resv_rate"])
    print("備轉容量率:", fore_peak_resv_rate)

    # 供電狀態
    power_status = ""
    fore_peak_resv_capacity = float(
        json["records"][1]["fore_peak_resv_capacity"])
    if fore_peak_resv_rate >= 10:
        power_status = "供電充裕"
    elif fore_peak_resv_rate < 10 and fore_peak_resv_rate >= 6:
        power_status = "供電吃緊"
    elif fore_peak_resv_rate < 6:
        power_status = "供電警戒"
        if fore_peak_resv_capacity <= 90:
            power_status = "限電警戒"
        elif fore_peak_resv_capacity <= 50:
            power_status = "限電準備"
    print("供電狀態:", power_status)

    data.append({
        "curr_load": curr_load,
        "curr_util_rate": curr_util_rate,
        "fore_peak_dema_load": fore_peak_dema_load,
        "fore_peak_dema_load_rate": fore_peak_dema_load_rate,
        "fore_peak_hour_range": fore_peak_hour_range,
        "fore_maxi_sply_capacity": fore_maxi_sply_capacity,
        "fore_peak_resv_rate": fore_peak_resv_rate,
        "power_status": power_status
    })

    # 寫入 database reference.
    doc_ref.set(data)
    print("\nTaiwan power updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan power updated")
