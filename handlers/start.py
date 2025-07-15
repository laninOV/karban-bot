from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# Тексты карточек "Что такое Карбан?"
about_cards = [
    "🌟 Карбан — это сообщество единомышленников, где каждый становится соавтором. Здесь ценится личный рост, поддержка и совместное творчество.",
    "🎯 В Karban ты проходишь философский тест, выбираешь свой путь (Резидент или Юн), получаешь доступ к личному кабинету, кошельку, дневнику и реферальной системе.",
    "⚡ Внутри — интерактив: вопрос дня, манифест, банк смыслов, мероприятия, геймификация и поддержка кураторов. Karban — среда для самореализации и новых связей."
]

async def start_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает стартовое меню при команде /start"""
    keyboard = [
        [InlineKeyboardButton("Хочу вступить", callback_data='join')],
        [InlineKeyboardButton("Что такое Карбан?", callback_data='about_card_0')],
        [InlineKeyboardButton("Пройти философский тест", callback_data='test')]
    ]
    
    text = ("Привет! Ты попал(а) в Karbан — среду единомышленников и нового типа взаимодействия. "
            "Здесь ты не просто участник — ты соавтор. Сделай первый шаг.")
    
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def join_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопки 'Хочу вступить' с описанием условий"""
    query = update.callback_query
    await query.edit_message_text(
        "💎 Условия вступления в Karban:\n\n"
        "• Доступ к закрытому сообществу единомышленников\n"
        "• Личный кабинет с KRB-кошельком и системой репутации\n"
        "• Персональный дневник для саморефлексии\n"
        "• Участие в мероприятиях и инициативах\n"
        "• Поддержка куратора @Василий\n"
        "• Стартовый набор: 50 KRB + 1 репутация\n\n"
        "Стоимость участия: [указать стоимость]\n"
        "Способы оплаты: [указать способы]\n\n"
        "Готов(а) присоединиться?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оплатить и вступить", callback_data='register')],
            [InlineKeyboardButton("Назад", callback_data='main_start')]
        ])
    )

async def about_card_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка карточек 'Что такое Карбан?'"""
    query = update.callback_query
    data = query.data
    idx = int(data.split("_")[-1])
    
    text = about_cards[idx]
    
    # Кнопки навигации
    buttons = []
    nav_row = []
    
    if idx > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"about_card_{idx - 1}"))
    if idx < len(about_cards) - 1:
        nav_row.append(InlineKeyboardButton("Далее ➡️", callback_data=f"about_card_{idx + 1}"))
    
    if nav_row:
        buttons.append(nav_row)
    
    buttons.append([InlineKeyboardButton("В главное меню", callback_data="main_start")])
    
    await query.edit_message_text(
        f"Карточка {idx + 1} из {len(about_cards)}\n\n{text}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Обработчики для экспорта
start_handler = CommandHandler("start", start_button)
start_menu_handler = CallbackQueryHandler(start_button, pattern="^main_start$")
join_handler = CallbackQueryHandler(join_button, pattern="^join$")
about_cards_handler = CallbackQueryHandler(about_card_handler, pattern="^about_card_[0-9]+$")
