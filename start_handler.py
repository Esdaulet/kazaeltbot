from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from reminder_handler import remind_membership, remind_membership_second # Импортируем функцию напоминания
from payment_handler import request_payment_receipt  # Подключаем необходимые функции
from approval_handler import handle_approval # Импортируем из нового файла
from reminder_handler import send_followup_message, handle_yes, handle_no # Импортируем функцию из reminder_handler
from datetime import timedelta


import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager_ids = [864464357,648034216]  # Замените числа на реальные ID всех менеджеров


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("✅ Yes!", callback_data="yes")],
        [InlineKeyboardButton("❌ No", callback_data="no")],
        [InlineKeyboardButton("ℹ️ Want to know more...", callback_data="more")],
        [InlineKeyboardButton("👤 I'm already member", callback_data="already_member")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        # Вызвано командой /start
        await update.message.reply_text(
            text = (
    "👋 **Welcome to the Association for the Professional Development of English Teachers in Kazakhstan!**\n\n"
    "We are delighted to have you join us on this journey of growth and professional development. Our community is "
    "dedicated to empowering English teachers across the country.\n\n"
    "✨ *Do YOU want to become a member of KAZAELT and be part of an inspiring network of educators?* ✨"
),

            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        # Вызвано кнопкой "Back"
        await update.callback_query.message.edit_text(
           "👋 **Welcome to the Association for the Professional Development of English Teachers in Kazakhstan!**\n\n"
    "We are delighted to have you join us on this journey of growth and professional development. Our community is "
    "dedicated to empowering English teachers across the country.\n\n"
    "✨ *Do YOU want to become a member of KAZAELT and be part of an inspiring network of educators?* ✨",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Проверяем, какую кнопку выбрал пользователь
   # Проверяем, какую кнопку выбрал пользователь
    if query.data == "yes" or query.data == "ready_to_join":
        new_keyboard = [
            [InlineKeyboardButton("🚀 GO", callback_data="go")],
            [InlineKeyboardButton("↩️ Back", callback_data="back")]
        ]
        new_reply_markup = InlineKeyboardMarkup(new_keyboard)
        await query.edit_message_text(
     "📚 **The Association for the Professional Development of English Teachers in Kazakhstan** \n\n"
    "Our mission is to support and empower English teachers across the country by enhancing their skills and knowledge\\. "
    "We provide engaging **workshops**, **seminars**, and a vibrant network of professionals, all designed to help you grow and succeed in your career.\n\n"
    "🌟 *Would you like to join us now?* 🌟",
    reply_markup=new_reply_markup,
    parse_mode="Markdown"

)

    elif query.data == "no":
        await query.edit_message_text("🙏Thank you for your interest! If you change your mind, we are always happy to welcome you into our ranks.")
        context.job_queue.run_once(remind_membership, timedelta(days=1).total_seconds(), data=query.message.chat_id)
    elif query.data == "notyet":
        await query.edit_message_text("✨ That’s perfectly fine! Take your time, and we’ll follow up with you soon.")
        context.job_queue.run_once(remind_membership, timedelta(days=1).total_seconds(), data=query.message.chat_id)
    elif query.data == "no_second":
        await query.edit_message_text(" 💭We understand completely! Feel free to take some more time to think it over.")
        context.job_queue.run_once(remind_membership_second, timedelta(weeks=1).total_seconds(), data=query.message.chat_id)
    elif query.data == "no_final":
        await query.edit_message_text(" 🌟Thanks for the reply. We respect your choice and will always be glad to see you in the future!")
    # Остальной код для других кнопок...
    elif query.data == "more":
        # Отправляем информацию о ссылках и кнопки "I've read" и "I'm ready to join"
        info_keyboard = [
            [InlineKeyboardButton("📖 Not ready yet", callback_data="notyet")],
            [InlineKeyboardButton("💪 I'm ready to join", callback_data="ready_to_join")]
        ]
        info_reply_markup = InlineKeyboardMarkup(info_keyboard)
        await query.edit_message_text(
            "🌐 Please have a look at the links below to know more about the association:\n\n"
            "Website: [kazaelt.kz](https://kazaelt.kz/) - Visit our website for comprehensive information about our activities, events, and resources.\n\n"
            "Annual conference website: [Tap here](https://kazaelt.kz/newconf)\n\n"
            "Social Media:\n- Instagram: [kazaelt](https://www.instagram.com/kazaelt?igsh=enQ4cGt5N3dzODc0)",
            reply_markup=info_reply_markup,
            parse_mode="Markdown"
        )
    elif query.data == "read":
        await query.edit_message_text("Thanks for the introduction!")
    elif query.data == "already_member":
        await query.edit_message_text("You are already a member! Thank you for your support!")
    elif query.data == "back":
        await start(update, context)  # Вернёт пользователя на начальную панель
    elif query.data == "go":
        # Информация об оплате
        payment_info = (
           "💳 *Great!* Thank you for your interest in joining the Kazakhstan Association of English Language Teachers.\n\n"
"You can learn more about our Association on our website: [KazAELT](https://kazaelt.kz), "
"and follow us on Instagram: [KazAELT Instagram](https://instagram.com/kazaelt?igshid=MzRlODBiNWFlZA==).\n\n"
"To make the payment via Kaspi, please use the following link. The membership fee for one person for 12 months is 25,000 KZT:\n"
"[Kaspi](https://kaspi.kz/pay/_gate?action=service_with_subservice&service_id=3025&subservice_id=18043&region_id=19)\n\n"
"Please select “Webinar” in the payment purpose. After making the payment, kindly send the receipt in PDF format."

        )

        # Клавиатура с кнопками оплаты
        payment_keyboard = [
            [InlineKeyboardButton("💰 Pay Now", url='https://kaspi.kz/pay/_gate?action=service_with_subservice&service_id=3025&subservice_id=18043&region_id=19')],
            [InlineKeyboardButton("📤 I have paid", callback_data='paid')],
            ##[InlineKeyboardButton("🔙 Back", callback_data='back_detailed')]
        ]
        payment_reply_markup = InlineKeyboardMarkup(payment_keyboard)

        # Отправляем сообщение об оплате
        await query.edit_message_text(
            text=payment_info,
            reply_markup=payment_reply_markup,
            parse_mode="Markdown"
        )
    if query.data == "paid":
        # Вызов функции для запроса изображения чека
        await request_payment_receipt(update, context)
    elif query.data == "back_detailed":
        # Возвращение к описанию ассоциации
        back_keyboard = [
            [InlineKeyboardButton("🚀 GO", callback_data="go")],
            [InlineKeyboardButton("↩️ Back", callback_data="back")]
        ]
        back_reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(
     "📚 **The Association for the Professional Development of English Teachers in Kazakhstan** \n\n"
    "Our mission is to support and empower English teachers across the country by enhancing their skills and knowledge\\. "
    "We provide engaging **workshops**, **seminars**, and a vibrant network of professionals, all designed to help you grow and succeed in your career.\n\n"
    "🌟 *Would you like to join us now?* 🌟",
     parse_mode="MarkdownV2",
    reply_markup=new_reply_markup
) 



    if not query or not query.from_user:
        logger.error("Ошибка: не удалось определить chat_id, query или from_user отсутствуют.")
        return  # Прерываем выполнение, если данных недостаточно

    # Отвечаем на callback_query
    await query.answer()

    chat_id = query.from_user.id
    logger.info(f"Попытка отправить сообщение пользователю с chat_id: {chat_id}")

    # Логика для обработки одобрения и отклонения
    if query.data.startswith("approve") or query.data.startswith("reject"):
        logger.info(f"Запущена handle_approval для callback_data: {query.data}")
        action, user_id = query.data.split("_")
        user_id = int(user_id)
        await handle_approval(update, context)  # Обработка в approval_handler

    # Логика для "charter_read"
    elif query.data == "charter_read":
        # Отправляем ссылку на Google Форму вместо текста "Thank you for reading the Charter!"
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please complete this form to continue:\n"
            "\n"
            "\n"
                 "https://docs.google.com/forms/d/e/1FAIpQLSdbORRAo-Ahp8T-XEgdnRNJl1R96m4wj1plj-b6og2oxPOU7A/viewform"
        )
        logger.info(f"Ссылка на форму отправлена пользователю {chat_id}")

        context.job_queue.run_once(send_followup_message, 10, data=chat_id)
    # Остальная логика обработки
    else:
        logger.info(f"Необработанное действие: {query.data}")
    
    if query.data == "completed_yes":
        await handle_yes(update, context)
    elif query.data == "completed_no":
        await handle_no(update, context)
    else:
        logger.info(f"Необработанное действие: {query.data}")



start_handler = CommandHandler("start", start)
button_handler = CallbackQueryHandler(button)
