from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes

async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает стартовое меню (по кнопке или при запуске)"""
    if update.message:
        # При /start
        await update.message.reply_text(
            "Привет! Ты попал(а) в Karbан — среду единомышленников и нового типа взаимодействия. "
            "Здесь ты не просто участник — ты соавтор. Сделай первый шаг.",
            reply_markup=main_keyboard()
        )
    elif update.callback_query:
        # При возврате по кнопке
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "Привет! Ты попал(а) в Karbан — среду единомышленников и нового типа взаимодействия. "
            "Здесь ты не просто участник — ты соавтор. Сделай первый шаг.",
            reply_markup=main_keyboard()
        )

def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Хочу вступить", callback_data='register')],
        [InlineKeyboardButton("Что такое Карбан?", callback_data='about')],
        [InlineKeyboardButton("Пройти философский тест", callback_data='test')]
    ])

# CallbackQueryHandler для возврата в главное меню
start_menu_handler = CallbackQueryHandler(start_button, pattern="^main_menu$")

# Для main.py:
# from handlers.start import start_button, start_menu_handler
# app.add_handler(start_menu_handler)
# app.add_handler(CommandHandler("start", start_button))
