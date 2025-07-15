# handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

about_cards = [
    "🌟 Karban — это сообщество единомышленников, где каждый становится соавтором. Здесь ценится личный рост и поддержка.",
    "🎯 Пройди тест, выбери путь (Резидент или Юн), получи доступ к личному кабинету, кошельку, рефкам, дневнику, геймификации.",
    "⚡ Интерактив: вопрос дня, манифест, банк смыслов, мероприятия и поддержка кураторов. Karban — среда самореализации."
]

async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Хочу вступить", callback_data='join')],
        [InlineKeyboardButton("Что такое Карбан?", callback_data='about_0')],
        [InlineKeyboardButton("Пройти философский тест", callback_data='test')]
    ]
    text = (
        "Привет! Ты попал(а) в Karban — среду единомышленников и нового типа взаимодействия. "
        "Здесь ты не просто участник — ты соавтор. Сделай первый шаг."
    )
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "💎 Условия вступления:\n"
        "- Доступ в сообщество единомышленников\n"
        "- Личный кабинет с KRB и репутацией\n"
        "- Персональный дневник\n"
        "- Реферальная система и геймификация\n"
        "- Поддержка куратора @Василий\n"
        "- Стартовый набор: 50 KRB + 1 реп\n\n"
        "Стоимость: [указать]\n"
        "Способы оплаты: [указать]",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оплатить и вступить", callback_data='register')],
            [InlineKeyboardButton("Назад в меню", callback_data='main')]
        ])
    )

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idx   = int(query.data.split("_")[1])
    text  = f"Карточка {idx+1}/{len(about_cards)}\n\n{about_cards[idx]}"
    buttons = []
    if idx > 0:
        buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"about_{idx-1}"))
    if idx < len(about_cards)-1:
        buttons.append(InlineKeyboardButton("Далее ➡️", callback_data=f"about_{idx+1}"))
    buttons.append(InlineKeyboardButton("В меню", callback_data='main'))
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([buttons]))

start_handler        = CommandHandler("start", start_button)
start_menu_handler   = CallbackQueryHandler(start_button, pattern="^main$")
join_handler         = CallbackQueryHandler(join_button, pattern="^join$")
about_cards_handler  = CallbackQueryHandler(about_handler, pattern="^about_[0-9]+$")
