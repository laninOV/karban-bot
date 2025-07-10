import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters
from config import ADMIN_IDS

USERS_FILE = "data/users.json"
TEST_QUESTIONS_FILE = "data/test_questions.json"

# --- Вспомогательные функции ---

def is_admin(user_id):
    return user_id in ADMIN_IDS

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_test_questions():
    if not os.path.exists(TEST_QUESTIONS_FILE):
        return []
    with open(TEST_QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_test_questions(questions):
    with open(TEST_QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

# --- Админ-панель через кнопки ---

async def admin_panel_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if not is_admin(user_id):
        await query.answer("Доступ запрещён.", show_alert=True)
        return

    keyboard = [
        [InlineKeyboardButton("Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton("Экспорт пользователей", callback_data="admin_export")],
        [InlineKeyboardButton("Редактировать тест", callback_data="admin_edit_test")],
    ]
    await query.edit_message_text(
        "Админ-панель Karban:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- Статистика ---

async def admin_stats_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not is_admin(query.from_user.id):
        await query.answer("Доступ запрещён.", show_alert=True)
        return
    users = load_users()
    total = len(users)
    residents = sum(1 for u in users.values() if u.get("archetype") == "Резидент")
    yuns = sum(1 for u in users.values() if u.get("archetype") == "Юн")
    await query.edit_message_text(
        f"Всего пользователей: {total}\n"
        f"Резидентов: {residents}\n"
        f"Юнов: {yuns}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="admin_panel")]
        ])
    )

# --- Рассылка ---

async def admin_broadcast_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not is_admin(query.from_user.id):
        await query.answer("Доступ запрещён.", show_alert=True)
        return
    context.user_data["admin_broadcast_mode"] = True
    await query.edit_message_text(
        "Введите текст для рассылки всем пользователям:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="admin_panel")]
        ])
    )

async def admin_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.user_data.get("admin_broadcast_mode"):
        return
    text = update.message.text
    users = load_users()
    count = 0
    for user_id in users.keys():
        try:
            await context.bot.send_message(chat_id=int(user_id), text=f"[Админ]: {text}")
            count += 1
        except Exception:
            continue
    await update.message.reply_text(f"Рассылка завершена. Сообщение отправлено {count} пользователям.")
    context.user_data["admin_broadcast_mode"] = False

# --- Экспорт пользователей ---

async def admin_export_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not is_admin(query.from_user.id):
        await query.answer("Доступ запрещён.", show_alert=True)
        return
    users = load_users()
    text = json.dumps(users, ensure_ascii=False, indent=2)
    if len(text) < 4000:
        await query.edit_message_text(f"Данные пользователей:\n{text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data="admin_panel")]
            ])
        )
    else:
        export_path = "data/export_users.json"
        with open(export_path, "w", encoding="utf-8") as f:
            f.write(text)
        await query.message.reply_document(document=InputFile(export_path), caption="Экспорт пользователей")
        await query.edit_message_text("Экспорт завершён.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Назад", callback_data="admin_panel")]
            ])
        )

# --- Редактирование теста ---

async def admin_edit_test_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not is_admin(query.from_user.id):
        await query.answer("Доступ запрещён.", show_alert=True)
        return
    questions = load_test_questions()
    text = "\n\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
    context.user_data["admin_edit_test_mode"] = True
    await query.edit_message_text(
        f"Текущие вопросы теста:\n{text}\n\n"
        "Отправьте новые вопросы одним сообщением, разделяя их двумя переносами строки.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Назад", callback_data="admin_panel")]
        ])
    )

async def admin_edit_test_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    if not context.user_data.get("admin_edit_test_mode"):
        return
    new_questions = update.message.text.strip().split("\n\n")
    save_test_questions(new_questions)
    await update.message.reply_text("Вопросы теста обновлены.")
    context.user_data["admin_edit_test_mode"] = False

# --- Router для CallbackQuery ---

async def admin_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "admin_panel":
        await admin_panel_button(update, context)
    elif data == "admin_stats":
        await admin_stats_button(update, context)
    elif data == "admin_broadcast":
        await admin_broadcast_button(update, context)
    elif data == "admin_export":
        await admin_export_button(update, context)
    elif data == "admin_edit_test":
        await admin_edit_test_button(update, context)

# --- Экспорт обработчиков для main.py ---

admin_router_handler = CallbackQueryHandler(admin_router, pattern="^admin_")
admin_broadcast_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, admin_broadcast_text)
admin_edit_test_text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, admin_edit_test_text)
