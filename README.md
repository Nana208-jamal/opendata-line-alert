# 雙北即時天候監控與跨日溫差警報推播系統

## 專案簡介
本專案為 Python 自動化資料處理應用，透過排程定時向開放資料平台（Open-Meteo API）發送請求，並利用 `Requests` 與 `JSONPath` 模組萃取即時氣象及日預報數據。當系統偵測到特定天候事件（例如降雨、極端高溫或跨日劇烈溫差）時，會即時整合預警資訊並透過 LINE Messaging API 推播至使用者手機。

## 系統特色與預警邏輯
1. **即時降雨偵測**：當前降雨量大於 0 mm 時，主動發送帶傘提醒。
2. **高溫炎熱警戒**：當前氣溫達到設定門檻（預設 28°C）時，發送防曬補水與防中暑警報。
3. **跨日溫差預警**：比對今日最高溫與明日預測最高溫，當溫差超過 3°C 時主動觸發「驟降添衣」或「明顯升溫」提示。
4. **自動定時監控**：使用 `schedule` 模組設定週期性定時任務（預設每 30 分鐘自動執行一次）。

## 使用技術與模組
- **Python 3**
- **Requests**：負責 API 的 HTTP 請求處理與資料獲取。
- **JSONPath**：快速定位並萃取巢狀 JSON 中的目標欄位（氣溫、降水量、跨日極端溫差等）。
- **Schedule**：管理背景定時監控排程。
- **LINE Messaging API**：實現客製化警報 Push Message 推播至行動裝置。

## 專案結構
```text
opendata-line-alert/
│
├── main.py              # 核心監控與推播腳本
├── requirements.txt     # Python 相依套件清單
└── README.md            # 專案說明與操作文件

執行與安裝說明
1. 安裝相依套件
在專案根目錄下開啟終端機並執行：

Bash
pip install -r requirements.txt
2. 環境變數 / 金鑰設定
在 main.py 中設定您的 LINE Messaging API 資訊：

Python
LINE_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
USER_ID = "YOUR_LINE_USER_ID"
3. 啟動程式
Bash
python main.py
程式啟動後將立即執行第一次天候檢測，隨後進入定時輪詢監控模式。