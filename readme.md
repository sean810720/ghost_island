<!--
 * @Author: Sean
 * @Date: 2021-05-25 16:51:42
 * @LastEditTime: 2021-05-25 17:22:16
-->

<p align="center"><h1>鬼島生存小本本 - 資料爬蟲</h1></p>
<p align="left">
API 目前已放上雲端，連結如下:<br/><br/>
(1) 台灣疫情日報<br/>
https://ghost-island-ab1d8-default-rtdb.firebaseio.com/covid-19/0.json
<br/><br/>
(2) 台電供電<br/>
https://ghost-island-ab1d8-default-rtdb.firebaseio.com/power/0.json
<br/><br/>
(3) 水庫水情<br/>
https://ghost-island-ab1d8-default-rtdb.firebaseio.com/water.json
</p>
<br/>

## 1. 套件安裝

pip3 install -r requirements.txt

## 2. 執行

### 台灣疫情日報
```
python3 covid-19.py
```

### 台電供電
```
python3 power.py
```

### 水庫水情
```
python3 water.py
```
