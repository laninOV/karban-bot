import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

# Кнопка для входа в дневник
async def diary_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        "Напиши свою запись в дневник одним сообщением. После отправки запись сохранится.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="main_menu")]
        ])
    )
    context.user_data["waiting_diary"] = True

# Обработка текстовой записи для дневника
async def diary_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_diary"):
        return
    user = update.effective_user
    users = load_users()
    user_id = str(user.id)
    text = update.message.text
    if user_id in users:
        users[user_id]["diary"] = text
        save_users(users)
        await update.message.reply_text("Запись сохранена в дневнике!")
    else:
        await update.message.reply_text("Сначала зарегистрируйтесь.")
    context.user_data["waiting_diary"] = False

# Обработчики для main.py
diary_handler = CallbackQueryHandler(diary_button, pattern="^diary$")
diary_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, diary_text)
