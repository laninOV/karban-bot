from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import KARBAN_CHAT_LINK, KARBAN_SITE

import json
import os

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает главное меню Karban"""
    keyboard = [
        [InlineKeyboardButton("Личный кабинет", callback_data='cabinet')],
        [InlineKeyboardButton("Сообщество", callback_data='community')],
        [InlineKeyboardButton("Философия", callback_data='philosophy')],
        [InlineKeyboardButton("О Karban", callback_data='about_menu')],
        [InlineKeyboardButton("Дневник", callback_data='diary')]
    ]
    text = "Главное меню Karban. Выбери раздел:"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = str(query.from_user.id)
    users = load_users()
    user = users.get(user_id, {})

    if data == "cabinet":
        # Показать личный кабинет с архетипом
        balance = user.get("krb", 0)
        rep = user.get("rep", 0)
        archetype = user.get("archetype", "Не определён")
        text = (
            f"🗝️ Личный кабинет:\n"
            f"Баланс: {balance} KRB\n"
            f"Репутация: {rep}\n"
            f"Архетип: {archetype}\n\n"
            "Выбери действие:"
        )
        keyboard = [
            [InlineKeyboardButton("В главное меню", callback_data="main_menu")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "community":
        await query.edit_message_text(
            f"🌐 Сообщество: {KARBAN_CHAT_LINK}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="main_menu")]])
        )

    elif data == "philosophy":
        await query.edit_message_text(
            "📜 Философия Karban:\n"
            "Мы верим в силу единства, осознанности и личностного роста.\n"
            "Вопрос дня: Какой твой главный смысл на сегодня?",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="main_menu")]])
        )

    elif data == "about_menu":
        await query.edit_message_text(
            f"ℹ️ О Karban:\n"
            f"Сайт: {KARBAN_SITE}\n"
            "Создатель: @founder\n"
            "Следите за событиями Karban!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="main_menu")]])
        )

    elif data == "diary":
        # Переходим в обработчик дневника
        await query.edit_message_text(
            "✍️ Дневник:\nНапиши свою запись одним сообщением.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data="main_menu")]])
        )
        context.user_data["waiting_diary"] = True

# Обработчики для main.py
send_main_menu_handler = CallbackQueryHandler(send_main_menu, pattern="^main_menu$")
menu_callback_handler = CallbackQueryHandler(menu_callback, pattern="^(cabinet|community|philosophy|about_menu|diary)$")
