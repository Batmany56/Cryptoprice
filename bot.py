import logging
import requests
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات خودت رو اینجا بذار (داخل دابل کوتیشن)
TOKEN = "9267113603:AAHIDxb_QSZ8GUOn8HDpwK7I4-vt5DpDMl4"

# تنظیم لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- بخش وب‌سرور برای Render ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- بخش ربات تلگرام ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 قیمت لحظه‌ای کریپتو", callback_data='crypto')],
        [InlineKeyboardButton("💵 دلار و طلا", callback_data='fiat')],
        [InlineKeyboardButton("⚠️ هشدارهای بازار", callback_data='alerts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات قیمت‌یاب خوش آمدید!\nیکی از گزینه‌ها رو انتخاب کنید:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'crypto':
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,tether,ripple&vs_currencies=usd"
            res = requests.get(url).json()
            text = f"💰 قیمت‌های لحظه‌ای:\n\n🔸 BTC: ${res['bitcoin']['usd']:,}\n🔸 ETH: ${res['ethereum']['usd']:,}\n🔸 BNB: ${res['binancecoin']['usd']:,}\n🔸 USDT: ${res['tether']['usd']:,}\n🔸 XRP: ${res['ripple']['usd']:,}"
            await query.edit_message_text(text)
        except:
            await query.edit_message_text("خطا در دریافت قیمت‌ها.")
    elif query.data == 'fiat':
        await query.edit_message_text("💵 قیمت‌های داخلی:\n\n💵 دلار: در حال دریافت...\n🥇 طلا: در حال دریافت...")
    elif query.data == 'alerts':
        await query.edit_message_text("⚠️ هشدارهای بازار:\n\nدر حال حاضر هشدار فعالی وجود ندارد.")

def main():
    # اجرای وب‌سرور در یک ترد جداگانه
    threading.Thread(target=run_web, daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
