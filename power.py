'''
Author: Sean
Date: 2021-05-23 01:44:57
LastEditTime: 2021-05-24 10:38:38
Description: Crawler of Taiwan power (台電電力供應)
FilePath: /Crawler/power.py
'''

import requests
import json

try:
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

    print("\nTaiwan power updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan power updated")
