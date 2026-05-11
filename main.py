
import telebot
import requests
from bs4 import BeautifulSoup
import time
import threading

# ضع التوكن الخاص بك هنا
API_TOKEN = 'ضع_هنا_توكن_بوت_فاذر'
bot = telebot.TeleBot(API_TOKEN)

URL = "https://adhahi.dz/register"
TARGET_STATE = "وهران" 

# ضع رقم الـ ID الخاص بك هنا بعد معرفته (سأخبرك كيف بعد قليل)
MY_CHAT_ID = None 

def check_website():
    while True:
        if MY_CHAT_ID:
            try:
                response = requests.get(URL, timeout=15)
                # إذا كانت الولاية موجودة في الصفحة
                if TARGET_STATE in response.text:
                    bot.send_message(MY_CHAT_ID, f"🚨 عاجل يا شمس الدين! تم فتح التسجيل في {TARGET_STATE} الآن! \nالرابط: {URL}")
                    # سيتوقف عن إرسال الرسائل لمدة ساعة بعد التنبيه لكي لا يزعجك
                    time.sleep(3600) 
            except Exception as e:
                print(f"Error checking site: {e}")
        time.sleep(60) # يفحص كل دقيقة

threading.Thread(target=check_website, daemon=True).start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global MY_CHAT_ID
    MY_CHAT_ID = message.chat.id
    bot.reply_to(message, f"تم تفعيل الرادار! 🎯\nرقم الـ ID الخاص بك هو: {MY_CHAT_ID}\nسأقوم بمراقبة ولاية {TARGET_STATE} وإخبارك فور فتحها.")

bot.polling()
