# main.py
from telegram.ext import ApplicationBuilder, CommandHandler

from config import TELEGRAM_TOKEN

from handlers.start        import start_handler, start_menu_handler, join_handler, about_cards_handler
from handlers.test         import test_handler, test_answer_handler, test_cancel_handler
from handlers.registration import registration_handler
from handlers.menu         import send_main_menu_handler, menu_callback_handler
from handlers.diary        import diary_handler, diary_text_handler
from handlers.admin        import admin_router_handler, admin_broadcast_text_handler, admin_edit_test_text_handler

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Стартовое меню
    app.add_handler(start_handler)
    app.add_handler(start_menu_handler)
    app.add_handler(join_handler)
    app.add_handler(about_cards_handler)

    # Философский тест
    app.add_handler(test_handler)
    app.add_handler(test_answer_handler)
    app.add_handler(test_cancel_handler)

    # Регистрация
    app.add_handler(registration_handler)

    # Главное меню
    app.add_handler(send_main_menu_handler)
    app.add_handler(menu_callback_handler)

    # Дневник
    app.add_handler(diary_handler)
    app.add_handler(diary_text_handler)

    # Админ-панель
    app.add_handler(admin_router_handler)
    app.add_handler(admin_broadcast_text_handler)
    app.add_handler(admin_edit_test_text_handler)

    print("Karban Bot запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
