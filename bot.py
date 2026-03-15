import os
from flask import Flask
from threading import Thread
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =========================================================
# 🛠️ لوحة التحكم - عدل هنا فقط لإضافة أي قسم أو أزرار
# =========================================================

# توكن البوت
TOKEN = "8718842894:AAGbG-lVSXN5NKssFgEXteTpVnzt-llHU2E"

# تعريف الأقسام ومحتوياتها
# كل مفتاح (Key) هو "اسم الزرار" اللي بيفتح القسم
MENU_STRUCTURE = {
    "الرئيسية": {
        "buttons": ["ما يخص المحاضرات", "ما يخص التاسكات"],
        "msg": "👋 مرحباً بك في أكاديمية DK R23\nاستخدم الأزرار بالأسفل للتنقل:"
    },
    
    "ما يخص المحاضرات": {
        "buttons": ["فيديوهات التشفير", "فيديوهات التلخيص", "رجوع"],
        "msg": "📚 قسم المحاضرات:\nاختر التصنيف الذي تريد الوصول إليه."
    },
    
    "فيديوهات التشفير": {
        "buttons": ["محاضرة 1", "محاضرة 2", "محاضرة 3", "محاضرة 4", "رجوع"],
        "msg": "🔐 إليك روابط فيديوهات برنامج التشفير:"
    },

    "فيديوهات التلخيص": {
        "buttons": ["تلخيص 1", "تلخيص 2", "رجوع"],
        "msg": "📺 إليك روابط فيديوهات التلخيص على يوتيوب:"
    },

    "ما يخص التاسكات": {
        "buttons": ["الربع الأول", "الربع الثاني", "الربع الثالث", "الربع الرابع", "رجوع"],
        "msg": "📝 قسم التاسكات:\nاختر الربع المطلوب لعرض التاسكات المتاحة."
    }
}

# الردود النهائية (اللينكات أو النصوص اللي بتظهر لما تضغط على زرار نهائي)
FINAL_RESPONSES = {
    "محاضرة 1": "🔗 رابط المحاضرة الأولى: [اضغط هنا](https://example.com)",
    "محاضرة 2": "🔗 رابط المحاضرة الثانية: [اضغط هنا](https://example.com)",
    "تلخيص 1": "📺 فيديو التلخيص الأول: [شاهد هنا](https://youtube.com/example)",
    "تاسك 1": "📌 المطلوب في تاسك 1 هو عمل كذا وكذا..",
    "default": "⚠️ هذا المحتوى سيتم إضافته قريباً، شكراً لصبرك."
}

# =========================================================
# 🌐 نظام الـ Keep Alive (لضمان بقاء البوت صاحياً)
# =========================================================
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# =========================================================
# ⚙️ المنطق البرمجي (لا يحتاج لتعديل غالباً)
# =========================================================

def get_keyboard(button_list):
    # تقسيم الأزرار لصفوف (كل صف زرارين)
    rows = [button_list[i:i + 2] for i in range(0, len(button_list), 2)]
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = MENU_STRUCTURE["الرئيسية"]
    await update.message.reply_text(content["msg"], reply_markup=get_keyboard(content["buttons"]))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # نظام الرجوع والقائمة الرئيسية
    if text == "رجوع" or text == "الرئيسية":
        await start(update, context)
        return

    # الانتقال بين القوائم
    if text in MENU_STRUCTURE:
        content = MENU_STRUCTURE[text]
        await update.message.reply_text(content["msg"], reply_markup=get_keyboard(content["buttons"]))
    
    # عرض الردود النهائية
    elif text in FINAL_RESPONSES:
        await update.message.reply_text(FINAL_RESPONSES[text], parse_mode='Markdown')
    
    # في حالة ضغط زرار ملوش محتوى لسه
    else:
        await update.message.reply_text(FINAL_RESPONSES["default"])

if __name__ == '__main__':
    keep_alive() # تشغيل سيرفر Flask
    print("Bot is starting...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
