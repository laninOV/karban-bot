# handlers/registration.py
import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from config import KARBAN_CHAT_LINK

USERS_FILE="data/users.json"
def load_users():
    return json.load(open(USERS_FILE,encoding="utf-8")) if os.path.exists(USERS_FILE) else {}
def save_users(u):
    json.dump(u, open(USERS_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid   = str(query.from_user.id)
    users = load_users()
    if users.get(uid,{}).get("registered"):
        return await query.edit_message_text(
            "Вы уже зарегистрированы!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("В меню", callback_data="main")]])
        )
    users.setdefault(uid,{})
    users[uid].update({"registered":True,"krb":50,"rep":1})
    save_users(users)
    await query.edit_message_text(
        f"🎉 Вы в Karban! Старт:50 KRB+1 реп\nЧат→{KARBAN_CHAT_LINK}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("В меню", callback_data="main")]])
    )

registration_handler = CallbackQueryHandler(register, pattern="^register$")
