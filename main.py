from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت (يفضل تغييره لاحقاً من BotFather للأمان)
TOKEN = "8718842894:AAGbG-lVSXN5NKssFgEXteTpVnzt-llHU2E"

# ---------------------------------------------------------
# لوحة التحكم في المحتوى - عدل هنا بسهولة من موبايلك
# ---------------------------------------------------------
BOT_CONTENT = {
    "الرئيسية": ["ما يخص المحاضرات", "ما يخص التاسكات"],
    
    "ما يخص المحاضرات": {
        "buttons": ["فيديوهات التشفير", "فيديوهات التلخيص", "الرئيسية"],
        "msg": "📚 قسم المحاضرات: اختر التصنيف المطلوب"
    },
    
    "فيديوهات التشفير": {
        "buttons": ["محاضرة 1", "محاضرة 2", "محاضرة 3", "رجوع"],
        "msg": "🔐 إليك لينكات فيديوهات برنامج التشفير:"
    },

    "فيديوهات التلخيص": {
        "buttons": ["تلخيص 1", "تلخيص 2", "رجوع"],
        "msg": "📺 إليك لينكات فيديوهات التلخيص على يوتيوب:"
    },

    "ما يخص التاسكات": {
        "buttons": ["الربع الأول", "الربع الثاني", "الربع الثالث", "الربع الرابع", "الرئيسية"],
        "msg": "📝 قسم التاسكات: اختر الربع المطلوب"
    },
    
    "responses": {
        "محاضرة 1": "🔗 لينك محاضرة 1: [اضغط هنا](https://example.com)",
        "تاسك 1": "📌 توصيف تاسك 1: المطلوب تسليم الملف بصيغة PDF.",
        "default": "⚠️ سيتم إضافة هذا المحتوى قريباً."
    }
}

def create_keyboard(button_list):
    keyboard = [button_list[i:i + 2] for i in range(0, len(button_list), 2)]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحباً بك في أكاديمية DK R23\nاستخدم الأزرار بالأسفل للتنقل:",
        reply_markup=create_keyboard(BOT_CONTENT["الرئيسية"])
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "الرئيسية" or text == "رجوع":
        await start(update, context)
        return

    if text in BOT_CONTENT and isinstance(BOT_CONTENT[text], dict):
        content = BOT_CONTENT[text]
        await update.message.reply_text(content["msg"], reply_markup=create_keyboard(content["buttons"]))
    elif text in BOT_CONTENT["responses"]:
        await update.message.reply_text(BOT_CONTENT["responses"][text], parse_mode='Markdown')
    else:
        await update.message.reply_text(BOT_CONTENT["responses"]["default"])

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
