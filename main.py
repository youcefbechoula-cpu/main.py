import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading

# ضع التوكن الخاص بك هنا
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

URL_ADHAHI = "https://adhahi.dz/register"
TARGET_STATE = "وهران" 
MY_CHAT_ID = None 

# --- وظيفة مراقبة الموقع (تعمل في الخلفية) ---
def check_website():
    while True:
        if MY_CHAT_ID:
            try:
                response = requests.get(URL_ADHAHI, timeout=15)
                if TARGET_STATE in response.text:
                    bot.send_message(MY_CHAT_ID, f"🚨 عاجل: تم فتح التسجيل في {TARGET_STATE} الآن! \nالرابط: {URL_ADHAHI}")
                    time.sleep(3600) # توقف ساعة بعد التنبيه
            except:
                pass
        time.sleep(60)

threading.Thread(target=check_website, daemon=True).start()

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global MY_CHAT_ID
    MY_CHAT_ID = message.chat.id
    bot.reply_to(message, f"🛡️ تم تشغيل البوت بنجاح!\n\n1. رادار وهران يعمل الآن 🎯\n2. أرسل اسم أي سكين CS2 لجلب سعره 💰")

@bot.message_handler(func=lambda message: True)
def get_price(message):
    skin_name = message.text
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={skin_name}"
        data = requests.get(url).json()
        if data.get("success"):
            price = data.get("lowest_price", "No price found")
            bot.reply_to(message, f"💰 Current Price: {price}")
        else:
            bot.reply_to(message, "❌ لم أجد هذا السكين. تأكد من الاسم بالإنجليزية.")
    except:
        bot.reply_to(message, "⚠️ حدث خطأ في جلب السعر.")

bot.polling()
