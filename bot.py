import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات خودت رو اینجا بذار (داخل دابل کوتیشن)
TOKEN = "9267113603:AAHIDxb_QSZ8GUOn8HDpwK7I4-vt5DpDMl4"

# تنظیم لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# منوی اصلی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 قیمت لحظه‌ای کریپتو", callback_data='crypto')],
        [InlineKeyboardButton("💵 دلار و طلا", callback_data='fiat')],
        [InlineKeyboardButton("⚠️ هشدارهای بازار", callback_data='alerts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به ربات قیمت‌یاب خوش آمدید!\nیکی از گزینه‌ها رو انتخاب کنید:", reply_markup=reply_markup)

# هندل کردن دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'crypto':
        # دریافت قیمت از CoinGecko
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,binancecoin,tether,ripple&vs_currencies=usd"
            res = requests.get(url).json()
            text = "💰 قیمت‌های لحظه‌ای:\n\n"
            text += f"🔸 BTC: ${res['bitcoin']['usd']:,}\n"
            text += f"🔸 ETH: ${res['ethereum']['usd']:,}\n"
            text += f"🔸 BNB: ${res['binancecoin']['usd']:,}\n"
            text += f"🔸 USDT: ${res['tether']['usd']:,}\n"
            text += f"🔸 XRP: ${res['ripple']['usd']:,}"
            await query.edit_message_text(text)
        except Exception as e:
            await query.edit_message_text("خطا در دریافت قیمت‌ها. لطفاً بعداً تلاش کنید.")

    elif query.data == 'fiat':
        # دریافت قیمت دلار و طلا (فعلاً به صورت تستی نوشته شده)
        text = "💵 قیمت‌های داخلی:\n\n"
        text += "💵 دلار: در حال دریافت...\n"
        text += "🥇 طلا (۱۸ عیار): در حال دریافت...\n"
        text += "(برای وصل کردن به API واقعی باید سرور Render رو ست کنیم)"
        await query.edit_message_text(text)

    elif query.data == 'alerts':
        text = "⚠️ هشدارهای بازار:\n\n"
        text += "در حال حاضر هشدار آنچینی فعالی وجود ندارد.\n"
        text += "(این بخش در نسخه‌های بعدی به DexScreener وصل می‌شود)"
        await query.edit_message_text(text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("ربات روشن شد...")
    app.run_polling()

if __name__ == '__main__':
    main()
