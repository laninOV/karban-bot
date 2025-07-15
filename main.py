from telegram.ext import ApplicationBuilder, CommandHandler
from config import TELEGRAM_TOKEN

# Стартовое меню и карточки
from handlers.start import (
    start_handler, 
    start_menu_handler, 
    join_handler, 
    about_cards_handler
)

# Философский тест
from handlers.test import test_handler, test_callback_handler

# Регистрация по кнопке
from handlers.registration import registration_handler

# Главное меню и переходы
from handlers.menu import menu_callback_handler

# Дневник (по кнопке и по тексту)
from handlers.diary import diary_handler, diary_text_handler

# Админ-панель (всё по кнопкам)
from handlers.admin import (
    admin_router_handler,
    admin_broadcast_text_handler,
    admin_edit_test_text_handler
)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Стартовое меню и связанные обработчики
    app.add_handler(start_handler)
    app.add_handler(start_menu_handler)
    app.add_handler(join_handler)
    app.add_handler(about_cards_handler)

    # Кнопки регистрации, теста, меню, дневника
    app.add_handler(registration_handler)
    app.add_handler(test_handler)
    app.add_handler(test_callback_handler)
    app.add_handler(menu_callback_handler)
    app.add_handler(diary_handler)
    app.add_handler(diary_text_handler)

    # Админ-панель и связанные функции (всё по кнопкам)
    app.add_handler(admin_router_handler)
    app.add_handler(admin_broadcast_text_handler)
    app.add_handler(admin_edit_test_text_handler)

    print("Karban Bot запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
