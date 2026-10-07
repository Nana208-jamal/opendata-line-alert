# 雙北即時天候監控與貼心生活警報推播系統 🌤️

## 專案簡介
本專案為基於 Python 實作的自動化資料擷取與推播應用。系統排程定時向氣象開放資料（Open Data）發送請求，運用 `Requests` 與 `JSONPath` 模組萃取即時氣候與日預報數據，並根據降雨、高溫及跨日劇烈溫差等多重條件進行智慧判定，最後透過 LINE Messaging API 主動將排版精緻的預警訊息推播至使用者的手機。

## 系統核心特色與預警邏輯
1. **即時降雨叮嚀**：當前累積降雨量大於 0 mm 時，主動發送帶傘提醒。
2. **高溫炎熱警戒**：當前氣溫達警戒門檻（預設 28°C）時，提示多補充水分與防曬。
3. **跨日溫差預警**：比對今日最高溫與明日預測最高溫，溫差達 3°C 以上時發送「驟降添衣」或「明顯升溫」提示。
4. **定時自動監控**：使用 `schedule` 模組背景輪詢，預設每 30 分鐘自動檢查一次。
5. **資安規範實作**：將敏感的 LINE 金鑰抽離至 `.env` 環境變數管理，並使用 `.gitignore` 隔離，避免 Token 外洩。

## 使用技術與模組
- **Python 3**
- **Requests**：發送 HTTP 請求擷取開放資料。
- **JSONPath**：快速定位並萃取巢狀 JSON 結構中的目標氣象欄位。
- **Schedule**：管理背景定時監控排程。
- **Python-dotenv**：載入本機環境變數保護 API 金鑰。
- **LINE Messaging API**：發送格式化 Push Message 至個人行動裝置。

## 專案結構
```text
opendata-line-alert/
│
├── main.py              # 核心監控與 LINE 推播腳本
├── requirements.txt     # Python 相依套件清單
├── .gitignore           # 排除 .env 等敏感檔案追蹤
├── .env                 # LINE 認證金鑰 (本地端配置，不推上 Git)
└── README.md            # 專案說明文件
執行與安裝說明
1. 安裝相依套件
在專案根目錄下開啟終端機並執行：

Bash
pip install -r requirements.txt
2. 環境變數設定
在專案根目錄下建立 .env 檔案，並填入您的 LINE Messaging API 資訊：

程式碼片段
LINE_ACCESS_TOKEN=YOUR_CHANNEL_ACCESS_TOKEN
LINE_USER_ID=YOUR_USER_ID
3. 啟動監控程式
Bash
python main.py
啟動後會立即執行第一次天候檢測並發送測試推播，隨後進入 30 分鐘週期的定時監控；若要退出程式，請在終端機按下 Ctrl + C。