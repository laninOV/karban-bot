# handlers/admin.py
import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters
from config import ADMIN_IDS

USERS_FILE = "data/users.json"
TEST_FILE  = "data/test_questions.json"

def load_users(): return json.load(open(USERS_FILE,encoding="utf-8")) if os.path.exists(USERS_FILE) else {}
def save_users(u): json.dump(u, open(USERS_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
def load_tests(): return json.load(open(TEST_FILE,encoding="utf-8")) if os.path.exists(TEST_FILE) else []
def save_tests(q):  json.dump(q, open(TEST_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

def is_admin(uid): return uid in ADMIN_IDS

async def admin_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; uid=q.from_user.id
    if not is_admin(uid): return await q.answer("Доступ запрещён.",show_alert=True)
    data=q.data
    if data=="admin": await show_panel(q)
    if data=="stats": await show_stats(q)
    if data=="broadcast": await ask_broadcast(q,context)
    if data=="export": await do_export(q)
    if data=="edit_test": await ask_edit(q,context)

async def show_panel(q):
    kb=[
      [InlineKeyboardButton("Статистика",        callback_data="stats")],
      [InlineKeyboardButton("Рассылка",          callback_data="broadcast")],
      [InlineKeyboardButton("Экспорт пользователей",callback_data="export")],
      [InlineKeyboardButton("Редактировать тест", callback_data="edit_test")]
    ]
    await q.edit_message_text("Админ-панель:",reply_markup=InlineKeyboardMarkup(kb))

async def show_stats(q):
    users=load_users()
    tot=len(users)
    res=sum(1 for u in users.values() if u.get("archetype")=="Резидент")
    yun=sum(1 for u in users.values() if u.get("archetype")=="Юн")
    await q.edit_message_text(f"Пользователей: {tot}\nРезидентов: {res}\nЮнов: {yun}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад",callback_data="admin")]]))

async def ask_broadcast(q,ctx):
    ctx.user_data["bc"]=True
    await q.edit_message_text("Введите текст рассылки:",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад",callback_data="admin")]]))

async def do_export(q):
    users=load_users()
    txt=json.dumps(users,ensure_ascii=False,indent=2)
    if len(txt)<4000:
        await q.edit_message_text(f"{txt}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад",callback_data="admin")]]))
    else:
        path="data/export_users.json"
        open(path,"w",encoding="utf-8").write(txt)
        await q.message.reply_document(document=InputFile(path))
        await q.edit_message_text("Экспорт готов.",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад",callback_data="admin")]]))

async def ask_edit(q,ctx):
    ctx.user_data["et"]=True
    qs=load_tests()
    text="\n\n".join(qs)
    await q.edit_message_text(f"Существующие:\n{text}\n\nОтправьте новые вопросы через два переноса строки.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад",callback_data="admin")]]))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid=update.effective_user.id
    if context.user_data.get("bc") and is_admin(uid):
        text=update.message.text
        cnt=0
        for u in load_users().keys():
            try: await update.bot.send_message(chat_id=int(u),text=text); cnt+=1
            except: pass
        await update.message.reply_text(f"Отправлено {cnt}")
        context.user_data["bc"]=False
    if context.user_data.get("et") and is_admin(uid):
        qs=update.message.text.split("\n\n")
        save_tests(qs)
        await update.message.reply_text("Тест обновлён")
        context.user_data["et"]=False

admin_router_handler         = CallbackQueryHandler(admin_router, pattern="^(admin|stats|broadcast|export|edit_test)$")
admin_broadcast_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
admin_edit_test_text_handler = admin_broadcast_text_handler
