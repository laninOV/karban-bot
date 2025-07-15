# handlers/diary.py
import json, os
from telegram import Update
from telegram.ext import MessageHandler, CallbackQueryHandler, ContextTypes, filters

USERS_FILE="data/users.json"
def load_users():
    return json.load(open(USERS_FILE,encoding="utf-8")) if os.path.exists(USERS_FILE) else {}
def save_users(u):
    json.dump(u, open(USERS_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

async def diary_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text("✍️ Напишите запись:")
    context.user_data["wait_diary"] = True

async def diary_txt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("wait_diary"): return
    uid = str(update.effective_user.id)
    users = load_users()
    users.setdefault(uid, {})["diary"] = update.message.text
    save_users(users)
    await update.message.reply_text("✅ Запись сохранена!")
    context.user_data["wait_diary"] = False
    # возврат в меню
    from handlers.menu import send_main
    await send_main(update, context)

diary_handler      = CallbackQueryHandler(diary_cb,   pattern="^diary$")
diary_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, diary_txt)
