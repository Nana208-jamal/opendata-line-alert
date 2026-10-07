import os
import time
import requests
import jsonpath
import schedule
from dotenv import load_dotenv

# 載入 .env 檔案裡的金鑰
load_dotenv()

# ======================= 設定區 =======================
API_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=25.03&longitude=121.56&"
    "current=temperature_2m,relative_humidity_2m,precipitation&"
    "daily=temperature_2m_max,temperature_2m_min&"
    "timezone=Asia%2FTaipei"
)

# 從環境變數讀取金鑰，如果找不到才用預設字串
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")

HOT_THRESHOLD = 28.0
TEMP_DIFF_THRESHOLD = 3.0
# =====================================================

# LINE Messaging API 設定 (保留你原本設定好的 Token 與 ID)
LINE_ACCESS_TOKEN = "NsxUfwaAmhaWkYPDTw9/Rdl+DdpWR9ilvwWpkuz/E+6HlGv0ikfnP/40Qon/8f37z73x7e8RNpwFYr7l3G7xSNMvnOnhKXTmxd62HA3fRgrASY2QCkZvCZxwT7DvGXTp+Dxo2acRkqaonxWdXHZumwdB04t89/1O/w1cDnyilFU="
USER_ID = "U11c473d1492da1297b0a445e39cbe7fe"

# 自訂警戒門檻
HOT_THRESHOLD = 28.0       # 氣溫超過此數值視為炎熱 (測試時可暫時改低，例如 20.0)
TEMP_DIFF_THRESHOLD = 3.0  # 兩天最高溫差達此數值觸發升/降溫警告
# =====================================================

def send_line_message(message_text: str):
    """發送 LINE 訊息通知"""
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message_text}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(">>> [LINE] 訊息發送成功！")
        else:
            print(f">>> [LINE] 發送失敗，狀態碼: {response.status_code}, 內容: {response.text}")
    except Exception as e:
        print(f">>> [LINE] 發送錯誤: {e}")

def monitor_opendata():
    """擷取 Open Data 並以 JSONPath 解析複合氣象預警"""
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 開始擷取 Open Data 氣象資料...")

    try:
        res = requests.get(API_URL, timeout=10)
        res.raise_for_status()
        data = res.json()

        # 1. 使用 JSONPath 萃取即時資料
        temp = float(jsonpath.jsonpath(data, "$.current.temperature_2m")[0])
        humidity = jsonpath.jsonpath(data, "$.current.relative_humidity_2m")[0]
        precip = float(jsonpath.jsonpath(data, "$.current.precipitation")[0])
        obs_time = jsonpath.jsonpath(data, "$.current.time")[0]

        # 2. 使用 JSONPath 萃取今明兩天最高溫
        today_max = float(jsonpath.jsonpath(data, "$.daily.temperature_2m_max[0]")[0])
        tomorrow_max = float(jsonpath.jsonpath(data, "$.daily.temperature_2m_max[1]")[0])
        temp_diff = round(tomorrow_max - today_max, 1)

        print(f"即時氣溫：{temp}°C | 降水量：{precip}mm | 今日最高：{today_max}°C | 明日最高：{tomorrow_max}°C")

        # 3. 複合警戒條件判斷
        # 3. 複合警戒條件判斷（精緻可愛版文案）
        warnings = []

        # 降雨提醒
        if precip > 0:
            warnings.append(f"🌧️ 外面正在飄雨（{precip} mm），出門記得把折疊傘放包包裡喔！")

        # 高溫提醒
        if temp >= HOT_THRESHOLD:
            warnings.append(f"🔥 當前氣溫偏高（{temp}°C），走在路上記得多喝水、做好防曬別中暑了～")

        # 溫差提醒
        if temp_diff <= -TEMP_DIFF_THRESHOLD:
            warnings.append(f"📉 明天最高溫比今天驟降了 {abs(temp_diff)}°C，早晚溫差大，出門加件薄外套喔！")
        elif temp_diff >= TEMP_DIFF_THRESHOLD:
            warnings.append(f"📈 明天最高溫會比今天上升 {temp_diff}°C，體感會變熱一些，穿搭可以輕便一點！")

        # 4. 組裝排版
        msg_lines = [
            "✨ ⸝⸝ 天氣即時速報 ⸝⸝ ✨",
            f"📍 觀測時間：{obs_time.replace('T', ' ')}",
            f"🌡️ 目前氣溫：{temp}°C（濕度 {humidity}%）",
            f"☀️ 今日最高：{today_max}°C ｜ 明日最高：{tomorrow_max}°C",
            "──────────────────"
        ]

        if warnings:
            msg_lines.append("💡 今日貼心小提醒：")
            for w in warnings:
                msg_lines.append(f"• {w}")
        else:
            msg_lines.append("🍃 目前天氣舒適宜人，出門一切順利，祝今天都有好心情 ☁️")

        full_message = "\n".join(msg_lines)
        send_line_message(full_message)

    except Exception as e:
        print(f"監測執行異常: {e}")

# ======================= 排程與主程式 =======================
if __name__ == "__main__":
    # 執行首次檢查
    monitor_opendata()

    # 設定定時排程：每 30 分鐘執行一次
    schedule.every(30).minutes.do(monitor_opendata)

    print("定時監控排程已啟動（每 30 分鐘檢查一次），按 Ctrl + C 可退出...")
    while True:
        schedule.run_pending()
        time.sleep(1)