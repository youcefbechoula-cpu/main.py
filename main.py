import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading

# التوكن الخاص بك تم وضعه هنا بنجاح
API_TOKEN = '8788543988:AAEiDekcxixlVlCjXm5pJ_otluPiBpTr_QY'
bot = telebot.TeleBot(API_TOKEN)

URL_ADHAHI = "https://adhahi.dz/register"
TARGET_STATE = "وهران" 
MY_CHAT_ID = None 

# --- وظيفة مراقبة موقع أضحيتي ---
def check_website():
    global MY_CHAT_ID
    while True:
        if MY_CHAT_ID:
            try:
                # محاولة جلب الصفحة
                response = requests.get(URL_ADHAHI, timeout=15)
                # فحص وجود كلمة وهران
                if TARGET_STATE in response.text:
                    bot.send_message(MY_CHAT_ID, f"🚨 عاجل يا شمس الدين! تم فتح التسجيل في {TARGET_STATE} الآن! \nالرابط: {URL_ADHAHI}")
                    time.sleep(3600) # يتوقف عن الإرسال لمدة ساعة لكي لا يزعجك
            except:
                pass
        time.sleep(60) # يفحص كل دقيقة

# تشغيل المراقبة في الخلفية
threading.Thread(target=check_website, daemon=True).start()

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global MY_CHAT_ID
    MY_CHAT_ID = message.chat.id
    bot.reply_to(message, f"🎯 تم تفعيل البوت بنجاح يا شمس الدين!\n\n1. رادار ولاية {TARGET_STATE} يعمل الآن.\n2. أرسل اسم أي سكين CS2 لجلب سعره.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    skin_name = message.text
    try:
        url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name={skin_name}"
        data = requests.get(url).json()
        if data.get("success"):
            price = data.get("lowest_price", "No price found")
            bot.reply_to(message, f"💰 Current Price: {price}")
        else:
            bot.reply_to(message, "❌ لم أجد هذا السكين. تأكد من كتابة الاسم بالإنجليزية بشكل دقيق.")
    except:
        bot.reply_to(message, "⚠️ خطأ في الاتصال بسوق ستيم.")

bot.polling()
