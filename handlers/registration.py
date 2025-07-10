import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import KARBAN_CHAT_LINK
from handlers.menu import send_main_menu  # Импортируйте функцию показа главного меню

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

async def registration_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопки регистрации"""
    query = update.callback_query
    user = query.from_user
    users = load_users()
    user_id = str(user.id)

    if user_id in users and users[user_id].get("registered"):
        await query.answer("Вы уже зарегистрированы!", show_alert=True)
        await query.edit_message_text(
            "Вы уже зарегистрированы!\n"
            f"Чат сообщества: {KARBAN_CHAT_LINK}"
        )
        await send_main_menu(update, context, user.id)
        return

    users[user_id] = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "registered": True,
        "krb": 50,
        "rep": 1,
        "archetype": users.get(user_id, {}).get("archetype", "Резидент"),
        "diary": "",
        "referrals": [],
        "influence": 0
    }
    save_users(users)

    await query.edit_message_text(
        "Поздравляем! Вы зарегистрированы в Karban.\n"
        f"Вот ваш стартовый набор:\n"
        f"- Ссылка в чат: {KARBAN_CHAT_LINK}\n"
        "- KRB-кошелек: 50 KRB\n"
        "- Куратор: @Василий\n\n"
        "Первое задание: Напишите в чат: «Меня зовут [имя], я хочу [цель]. Кто готов помочь?» и заработайте 2 KRB +1 Реп."
    )

    await send_main_menu(update, context, user.id)

# Обработчик для main.py:
registration_handler = CallbackQueryHandler(registration_button, pattern="^register$")

# В стартовом меню (например, в handlers/start.py) используйте кнопку:
# InlineKeyboardButton("Хочу вступить", callback_data="register")
