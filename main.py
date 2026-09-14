import os
import requests

# 1. 設定經緯度 (預設以台北為例：緯度 25.0375, 經度 121.5637，可依需求自行修改)
LATITUDE = 25.0375
LONGITUDE = 121.5637

# 2. 透過環境變數讀取 Telegram 金鑰（避免硬寫在程式碼中）
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def get_precipitation_probability():
    """透過 Open-Meteo API 取得今日最高降雨機率"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "daily": "precipitation_probability_max",
        "timezone": "Asia/Taipei",
        "forecast_days": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # 取得今天最高降雨機率 (%)
        pop_max = data["daily"]["precipitation_probability_max"][0]
        return pop_max
    except Exception as e:
        print(f"取得天氣資料失敗: {e}")
        return None


def send_telegram_message(message):
    """傳送訊息至 Telegram Bot"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("錯誤：未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID 環境變數。")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Telegram 通知傳送成功！")
    except Exception as e:
        print(f"傳送 Telegram 訊息失敗: {e}")


def main():
    pop = get_precipitation_probability()

    if pop is None:
        print("無法取得降雨機率，結束程式。")
        return

    print(f"今日最高降雨機率為: {pop}%")

    # 3. 判斷降雨機率是否超過 30%
    if pop > 30:
        message = f"🌧️【下雨提醒】今天最高降雨機率為 {pop}%，出門記得帶傘喔！"
        send_telegram_message(message)
    else:
        print("降雨機率未超過 30%，不發送通知。")


if __name__ == "__main__":
    main()
