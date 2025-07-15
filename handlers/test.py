# handlers/test.py
import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes

USERS_FILE = "data/users.json"
def load_users():
    return json.load(open(USERS_FILE, encoding="utf-8")) if os.path.exists(USERS_FILE) else {}
def save_users(u):
    json.dump(u, open(USERS_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

questions = [
    ("Какой тип мышления ближе?", [("Аналитический","A"),("Интуитивный","B")]),
    ("Что важнее в жизни?",      [("Стабильность","A"),("Развитие","B")]),
    ("Чего боишься больше?",     [("Одиночество","A"),("Ограничения","B")]),
    ("Формат самореализации?",   [("В команде","A"),("Индивидуально","B")]),
    ("Подход к проблемам?",      [("Системно","A"),("Творчески","B")])
]
archetypes = {
    "Резидент": "Ты — Резидент Karban! Ты ценишь порядок и командную работу.",
    "Юн":       "Ты — Юн Karban! Ты склонен к экспериментам и новым идеям."
}

def calc(answers):
    return "Резидент" if answers.count("A")>=3 else "Юн"

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid   = str(query.from_user.id)
    context.user_data[uid] = {"ans":[], "i":0}
    await send_q(query, context, uid)

async def send_q(query, context, uid):
    data = context.user_data[uid]
    i    = data["i"]
    if i >= len(questions):
        return await finish_test(query, context, uid)
    q, opts = questions[i]
    kb = [[InlineKeyboardButton(text, callback_data=f"ans_{val}")] for text,val in opts]
    kb.append([InlineKeyboardButton("Отмена", callback_data="test_cancel")])
    await query.edit_message_text(f"Вопрос {i+1}/{len(questions)}\n\n{q}", reply_markup=InlineKeyboardMarkup(kb))

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid   = str(query.from_user.id)
    data  = query.data.split("_")[1]
    ud    = context.user_data.get(uid)
    if not ud: return
    ud["ans"].append(data)
    ud["i"] += 1
    await send_q(query, context, uid)

async def finish_test(query, context, uid):
    ans = context.user_data[uid]["ans"]
    arch = calc(ans)
    users = load_users()
    users.setdefault(uid, {})["archetype"] = arch
    save_users(users)
    text = f"{archetypes[arch]}\n\nКак Karban поможет тебе раскрыть потенциал?"
    kb = [
        [InlineKeyboardButton("Зарегистрироваться", callback_data="register")],
        [InlineKeyboardButton("В меню",            callback_data="main")]
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    context.user_data.pop(uid, None)

async def cancel_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "Тест отменён.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("В меню", callback_data="main")]])
    )

test_handler         = CallbackQueryHandler(start_test, pattern="^test$")
test_answer_handler  = CallbackQueryHandler(answer,    pattern="^ans_[AB]$")
test_cancel_handler  = CallbackQueryHandler(cancel_test,pattern="^test_cancel$")
