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
    url = "https://api.coinpaprika.com/v1/tickers"
    response = requests.get(url)
    try:
        data = response.json()
        top_10 = sorted(data, key=lambda x: x['rank'])[:10]
        return top_10
    except Exception as e:
        print("❌ JSON xatosi:", e)
        print("❌ API javobi (matn):", response.text)
        raise e

def make_message(data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = f"📊 <b>Top 10 Kripto Kurslari</b>\n🕘 {now} (Toshkent vaqti)\n\n"
    for i, coin in enumerate(data, 1):
        name = coin['name']
        symbol = coin['symbol']
        price = round(coin['quotes']['USD']['price'], 2)
        message += f"{i}. {name} ({symbol}) — ${price}\n"
    message += "\n🔗 <a href='https://coinpaprika.com'>Top 100 uchun bosing</a>"
    return message

if __name__ == "__main__":
    try:
        cryptos = get_top_10_cryptos()
        print("✅ Crypto ma'lumotlar olindi")
        msg = make_message(cryptos)
        print("✅ Xabar tayyorlandi")
        bot.send_message(chat_id=CHANNEL_USERNAME, text=msg, parse_mode="HTML", disable_web_page_preview=True)
        print("✅ Xabar yuborildi")
    except Exception as e:
        print(f"Xatolik: {e}")

