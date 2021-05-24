'''
Author: Sean
Date: 2021-05-22 23:21:42
LastEditTime: 2021-05-24 10:34:26
Description: Crawler of Taiwan Covid-19 statistics (台灣疫情報告)
FilePath: /Crawler/covid-19.py
'''

import requests
from bs4 import BeautifulSoup

try:

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

    # 解除隔離
    recovered = "0" if len(soup.select(
        ".country_recovered")) == 0 else soup.select(".country_recovered")[0].text
    print("解除隔離:", recovered)

    # 病死率
    rate_deaths = "0%" if len(soup.select(
        "#country_cfr")) == 0 else soup.select("#country_cfr")[0].text
    print("病死率:", rate_deaths)

    # 新增確診
    new_confirmed = "0" if len(soup.select(
        ".country_confirmed_change")) == 0 else soup.select(".country_confirmed_change")[0].text
    if len(new_confirmed.strip()) == 0:
        new_confirmed = "0"
    print("新增確診:", new_confirmed)

    # 新增死亡
    new_deaths = "0" if len(soup.select(
        ".country_deaths_change")) == 0 else soup.select(".country_deaths_change")[0].text
    if len(new_deaths.strip()) == 0:
        new_deaths = "0"
    else:
        new_deaths = new_deaths.split("+ ")[1]
    print("新增死亡:", new_deaths)

    print("\nTaiwan Covid-19 statistics updated")

except Exception as e:
    print('\n錯誤訊息:', e)
    print("\nTaiwan Covid-19 statistics updated")
