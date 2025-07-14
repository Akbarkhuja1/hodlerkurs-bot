import os
import requests
from datetime import datetime
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
print("BOT_TOKEN:", BOT_TOKEN)
print("CHANNEL_USERNAME:", CHANNEL_USERNAME)

bot = Bot(token=BOT_TOKEN)

def get_top_10_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    try:
        data = response.json()
    except Exception as e:
        print("JSON olishda xatolik:", e)
        print("API javobi (text):", response.text)
        raise e
    return data

def make_message(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📊 <b>Top 10 Kripto Kurslari</b>\n🕘 {now} (Toshkent vaqti)\n\n"
    for i, coin in enumerate(data, 1):
        name = coin['name']
        price = round(coin['current_price'], 2)
        symbol = coin['symbol'].upper()
        message += f"{i}. {name} ({symbol}) — ${price}\n"
    message += "\n🔗 <a href='https://www.coingecko.com'>Top 100 uchun bosing</a>"
    return message

if __name__ == "__main__":
    try:
        cryptos = get_top_10_cryptos()
        msg = make_message(cryptos)
        bot.send_message(chat_id=CHANNEL_USERNAME, text=msg, parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        print(f"Xatolik: {e}")
