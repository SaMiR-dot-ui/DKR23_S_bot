
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8718842894:AAGbG-lVSXN5NKssFgEXteTpVnzt-llHU2E"

# القائمة الرئيسية
def main_menu():
    keyboard = [
        [InlineKeyboardButton("المحاضرات", callback_data="lectures")],
        [InlineKeyboardButton("التاسكات", callback_data="tasks")]
    ]
    return InlineKeyboardMarkup(keyboard)

# قائمة المحاضرات
def lectures_menu():
    keyboard = [
        [InlineKeyboardButton("لينكات فيديوهات برنامج التشفير", callback_data="encrypt_videos")],
        [InlineKeyboardButton("لينكات فيديوهات التلخيص على يوتيوب", callback_data="summary_videos")],
        [InlineKeyboardButton("⬅ رجوع", callback_data="main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def lectures_list(parent):
    keyboard = []
    for i in range(1,6):
        keyboard.append([InlineKeyboardButton(f"محاضرة {i}", callback_data=f"lecture_{i}")])
    keyboard.append([InlineKeyboardButton("⬅ رجوع", callback_data=parent)])
    return InlineKeyboardMarkup(keyboard)

# قائمة الأرباع
def quarters_menu():
    keyboard = [
        [InlineKeyboardButton("الربع الاول", callback_data="q1")],
        [InlineKeyboardButton("الربع الثاني", callback_data="q2")],
        [InlineKeyboardButton("الربع الثالث", callback_data="q3")],
        [InlineKeyboardButton("الربع الرابع", callback_data="q4")],
        [InlineKeyboardButton("⬅ رجوع", callback_data="main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def tasks_list():
    keyboard = []
    for i in range(1,6):
        keyboard.append([InlineKeyboardButton(f"تاسك {i}", callback_data=f"task_{i}")])
    keyboard.append([InlineKeyboardButton("⬅ رجوع", callback_data="tasks")])
    return InlineKeyboardMarkup(keyboard)

def task_details():
    keyboard = [
        [InlineKeyboardButton("توصيف تاسك", callback_data="desc")],
        [InlineKeyboardButton("ملفات مرفقة", callback_data="files")],
        [InlineKeyboardButton("استفسارات", callback_data="questions")],
        [InlineKeyboardButton("⬅ رجوع", callback_data="tasks_list")]
    ]
    return InlineKeyboardMarkup(keyboard)

def questions_menu():
    keyboard = []
    for i in range(1,6):
        keyboard.append([InlineKeyboardButton(f"استفسار {i}", callback_data="answer")])
    keyboard.append([InlineKeyboardButton("⬅ رجوع", callback_data="task_details")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "اهلا بيك في بوت DK R23\nاكاديمية دار الكهربا لتدريب المهندسين\n\nاختر الخدمة:",
        reply_markup=main_menu()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await query.edit_message_text("اختر الخدمة:", reply_markup=main_menu())
    elif data == "lectures":
        await query.edit_message_text("قسم المحاضرات:", reply_markup=lectures_menu())
    elif data == "encrypt_videos":
        await query.edit_message_text("اختر المحاضرة:", reply_markup=lectures_list("lectures"))
    elif data == "summary_videos":
        await query.edit_message_text("اختر المحاضرة:", reply_markup=lectures_list("lectures"))
    elif data.startswith("lecture_"):
        await query.edit_message_text("سيتم إضافة لينك المحاضرة هنا لاحقاً.",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ رجوع", callback_data="lectures")]]))
    elif data == "tasks":
        await query.edit_message_text("اختر الربع:", reply_markup=quarters_menu())
    elif data in ["q1","q2","q3","q4"]:
        await query.edit_message_text("اختر التاسك:", reply_markup=tasks_list())
    elif data.startswith("task_"):
        await query.edit_message_text("تفاصيل التاسك:", reply_markup=task_details())
    elif data == "tasks_list":
        await query.edit_message_text("اختر التاسك:", reply_markup=tasks_list())
    elif data == "task_details":
        await query.edit_message_text("تفاصيل التاسك:", reply_markup=task_details())
    elif data == "desc":
        await query.edit_message_text("سيتم إضافة توصيف التاسك هنا.",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ رجوع", callback_data="task_details")]]))
    elif data == "files":
        await query.edit_message_text("سيتم إضافة الملفات هنا.",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ رجوع", callback_data="task_details")]]))
    elif data == "questions":
        await query.edit_message_text("اختر الاستفسار:", reply_markup=questions_menu())
    elif data == "answer":
        await query.edit_message_text("اجابة",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅ رجوع", callback_data="questions")]]))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
