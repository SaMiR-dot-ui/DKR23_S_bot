import os
from flask import Flask
from threading import Thread
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ===========================
# توكن البوت
# ===========================
TOKEN = "8718842894:AAGbG-lVSXN5NKssFgEXteTpVnzt-llHU2E"

# ===========================
# تعريف القوائم والأزرار
# ===========================
MENU_STRUCTURE = {
    "الرئيسية": {
        "buttons": ["محاضرات", "تاسكات"],
        "msg": "اختر القسم:"
    },
    
    "محاضرات": {
        "buttons": ["الربع الاول", "الربع الثاني", "الربع الثالث", "الربع الرابع"],
        "msg": "اختر الربع:"
    },
    
    "الربع الاول": {
        "buttons": [
            "DIALux Software", "Lighting Design", "Power and MEP Design", 
            "Panel Schedule", "Cutting List + ETAP", "Equipment Sizing + SLD", "Load Estimation + HVAC Design"
        ],
        "msg": "اختر الموضوع:"
    },
    
    "الربع الثاني": {
        "buttons": [
            "Fire Alarm", "Data & Telephone + Public Adress", 
            "CCTV + Access Control + Parking System", "NCS + Audio Visual + TV",
            "QS + BOQ + IFC"
        ],
        "msg": "اختر الموضوع:"
    },
    
    "الربع الثالث": {
        "buttons": [
            "Site Implementation + Method of Statements", "PWR SD", "LTG SD", "Hatch Mark",
            "Single Line Routing", "Cable Routing SD", "LC SD", "VE + MS + LOG + Client", "Installation Workshop"
        ],
        "msg": "اختر الموضوع:"
    },
    
    "الربع الرابع": {
        "buttons": ["Straight Elements", "Average Length", "Outlets", "Decvices", "Contract Drafts"],
        "msg": "اختر الموضوع:"
    },
    
    "تاسكات": {
        "buttons": ["الربع الاول", "الربع الثاني", "الربع الثالث", "الربع الرابع"],
        "msg": "اختر الربع:"
    },
}

# الردود الفرعية لكل موضوع في المحاضرات
SUB_MENU_LECTURES = ["برنامج التشفير", "فيديو التلخيص"]

# الردود الفرعية لكل موضوع في التاسكات
SUB_MENU_TASKS = ["توصيف التاسك", "ملفات مرفقة", "استفسارات"]

# الردود النهائية للمواضيع (مثال)
FINAL_RESPONSES = {
    "برنامج التشفير": "رابط برنامج التشفير سيتم إضافته هنا.",
    "فيديو التلخيص": "رابط فيديو التلخيص سيتم إضافته هنا.",
    "توصيف التاسك": "توصيف التاسك سيتم إضافته هنا.",
    "ملفات مرفقة": "الملفات المرفقة ستظهر هنا.",
    "استفسارات": "الردود على الاستفسارات ستظهر هنا.",
    "default": "المحتوى سيتم إضافته قريباً."
}

# ===========================
# نظام Keep Alive
# ===========================
app = Flask('')

@app.route('/')
def home():
    return "Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===========================
# دوال مساعدة
# ===========================
def get_keyboard(button_list, add_back_buttons=True, menu_type="lecture"):
    """
    توليد لوحة الأزرار مع الزرين الثابتين في الأسفل (رجع خطوة / الرئيسية)
    button_list: قائمة الأزرار العلوية
    add_back_buttons: إضافة أزرار الرجوع أم لا
    menu_type: "lecture" أو "task" لتحديد الفرعي
    """
    # تقسيم الأزرار لصفوف (كل صف زر واحد فقط لتكون فوق بعض)
    rows = [[btn] for btn in button_list]
    
    # إضافة الزرين الثابتين في الأسفل
    if add_back_buttons:
        rows.append(["رجع خطوة", "الرئيسية"])
    
    return ReplyKeyboardMarkup(rows, resize_keyboard=True)

# ===========================
# المنطق البرمجي
# ===========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = MENU_STRUCTURE["الرئيسية"]
    await update.message.reply_text(content["msg"], reply_markup=get_keyboard(content["buttons"], add_back_buttons=False))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # الرجوع
    if text == "الرئيسية":
        await start(update, context)
        return
    if text == "رجع خطوة":
        # نقدر نخلي الرجوع للوالد مباشرة (هنا افتراضياً نرجع للرئيسية)
        await start(update, context)
        return

    # القوائم الرئيسية والفرعية
    if text in MENU_STRUCTURE:
        content = MENU_STRUCTURE[text]
        await update.message.reply_text(content["msg"], reply_markup=get_keyboard(content["buttons"]))
        return

    # المواضيع النهائية للمحاضرات
    if text in SUB_MENU_LECTURES or text in SUB_MENU_TASKS:
        if text in FINAL_RESPONSES:
            await update.message.reply_text(FINAL_RESPONSES[text])
        else:
            await update.message.reply_text(FINAL_RESPONSES["default"])
        return

    # مواضيع محددة في كل ربع
    if text in FINAL_RESPONSES:
        await update.message.reply_text(FINAL_RESPONSES[text])
        return

    # زرار افتراضي
    await update.message.reply_text(FINAL_RESPONSES["default"])

# ===========================
# التشغيل
# ===========================
if __name__ == '__main__':
    keep_alive()
    print("Bot is starting...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()