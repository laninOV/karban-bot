from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes

# Пример вопросов теста
test_questions = [
    "1. Какой тип мышления тебе ближе?\nA) Аналитический\nB) Интуитивный",
    "2. Что для тебя важнее?\nA) Самореализация\nB) Признание",
    "3. Чего ты боишься больше?\nA) Одиночества\nB) Неуспеха",
    "4. Какой формат самореализации тебе ближе?\nA) Работа в команде\nB) Самостоятельные проекты"
]

test_results = {
    'AAAA': 'Резидент',
    'AAAB': 'Резидент',
    'AABA': 'Юн',
    'AABB': 'Юн',
    'ABAA': 'Резидент',
    'ABAB': 'Юн',
    'ABBA': 'Юн',
    'ABBB': 'Юн',
    'BAAA': 'Юн',
    'BAAB': 'Юн',
    'BABA': 'Резидент',
    'BABB': 'Резидент',
    'BBAA': 'Юн',
    'BBAB': 'Юн',
    'BBBA': 'Резидент',
    'BBBB': 'Юн'
}

async def test_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    context.user_data[user_id] = {"answers": "", "step": 0}
    await send_test_question(query, context, user_id)

async def test_callback_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = context.user_data.get(user_id, {"answers": "", "step": 0})
    answer = query.data.split("_")[1]
    data["answers"] += answer
    data["step"] += 1
    context.user_data[user_id] = data

    if data["step"] < len(test_questions):
        await send_test_question(query, context, user_id)
    else:
        result_key = data["answers"].ljust(4, 'A')
        archetype = test_results.get(result_key, 'Резидент')
        await query.edit_message_text(
            f"Твой архетип: {archetype}\nKarban поможет тебе раскрыть потенциал и найти единомышленников.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Вернуться в меню", callback_data="main_menu")]
            ])
        )

async def send_test_question(query, context, user_id):
    data = context.user_data[user_id]
    step = data["step"]
    question = test_questions[step]
    keyboard = [
        [
            InlineKeyboardButton("A", callback_data='test_A'),
            InlineKeyboardButton("B", callback_data='test_B')
        ]
    ]
    await query.edit_message_text(question, reply_markup=InlineKeyboardMarkup(keyboard))

# Экспорт обработчиков для main.py
test_handler = CallbackQueryHandler(test_handler_fn, pattern="^test$")
test_callback_handler = CallbackQueryHandler(test_callback_handler_fn, pattern="^test_[AB]$")
