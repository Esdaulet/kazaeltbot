from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from start_handler import start_handler, button_handler, button
from payment_handler import handle_pdf
from approval_handler import handle_approval
from city_question import ask_city_question, handle_city_selection


# Импорт других обработчиков

def main():
    application = Application.builder().token("7542003409:AAGfKAll0ZxXgL_V9i5mF5u0SM1YQfR25Tg").build()
    
    # Регистрация обработчиков
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(handle_city_selection, pattern="^(Toleby region|Karaganda|Uralsk|Taraz|Zhanaozen|Astana|Oskemen, Ridder|Almaty region|Almaty|Turkistan region|Semey|Shymkent|North KZ region|Kyzylorda|Pavlodar|Aktau|Kokshetau|Aktobe|Atyrau|Kostanay|Taldykorgan|Kazgurt)$"))
    application.add_handler(button_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_pdf))  # Фильтр для всех документов и изображений
    application.add_handler(CallbackQueryHandler(handle_approval, pattern="^(approve|reject)_"))
    application.add_handler(CallbackQueryHandler(handle_approval, pattern="charter_read"))  # Регистрация для "charter_read"

    # Добавить другие обработчики
    
    application.run_polling()

if __name__ == '__main__':

    main()
