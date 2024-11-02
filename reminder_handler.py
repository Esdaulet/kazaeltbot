from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from city_question import ask_city_question  # Импортируем новую функцию
import logging


logger = logging.getLogger(__name__)


async def remind_membership(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создаём кнопки для повторного вопроса
    keyboard = [
        [InlineKeyboardButton("✅ Yes!", callback_data="yes")],
        [InlineKeyboardButton("❌ No", callback_data="no_second")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=context.job.data,
        text="It hasn't been long! Have you changed your mind? Do you want to become a member of the association?",
        reply_markup=reply_markup
    )

async def remind_membership_second(context: ContextTypes.DEFAULT_TYPE) -> None:
    # Второе напоминание через 20 секунд
    keyboard = [
        [InlineKeyboardButton("✅ Yes!", callback_data="yes")],
        [InlineKeyboardButton("❌ No", callback_data="no_final")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=context.job.data,
        text="Мы снова спрашиваем: Хотите стать членом ассоциации? Это последнее предложение!",
        reply_markup=reply_markup
    )

async def send_followup_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение через 30 секунд после отправки ссылки на регистрацию"""
    chat_id = context.job.data  # Используем context.job.data
    await context.bot.send_message(
        chat_id=chat_id,
        text="Have you completed the registration form? Please select an option below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Yes", callback_data="completed_yes")],
            [InlineKeyboardButton("No", callback_data="completed_no")]
        ])
    )

async def handle_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие кнопки 'Yes' и отправляет приветственное сообщение"""
    chat_id = update.callback_query.from_user.id
    await context.bot.send_message(
        chat_id=chat_id,
        text=(
        "Welcome to Kazaelt!\n\n"
        "We are delighted to have you join our community. Here’s all the information you need to get started:\n\n"
        "Website: [kazaelt.kz](https://kazaelt.kz/)\n"
        "Visit our website for comprehensive information about our activities, events, and resources.\n\n"
        "Annual conference website: [Tap here](https://kazaelt.kz/newconf)\n\n"
        "Social Media:\n"
        "- Instagram: [kazaelt](https://www.instagram.com/kazaelt?igsh=enQ4cGt5N3dzODc0)\n"
        "- Telegram Channel: [KazAELT members](https://t.me/+B0WNvNnla_Q2NDMy) | [Kazaelt on Air](https://t.me/kazaelt)\n\n"
        "Speaking Club:\n"
        "Join our Speaking Club every day at 8:00 p.m. [Join here](https://chat.whatsapp.com/JoK0Hm29bs33vyyuuD3s1R)\n\n"
        "Feel free to ask any questions [here](https://t.me/c/1864095672/2659).\n\n"
        "We are here to support each other and develop together.\n\n"
        "All questions can be written in the [Q&A chat](https://t.me/c/1864095672/2659).\n\n"
        "Local coordinators are also available to help you. To find the contact details of your regional coordinator, "
        "please reach out to the head of the coordinators: Gulfairuz teacher\n\n"
        "Membership manager: Aizhan teacher\n\n"
        "Once again, welcome to Kazaelt! We look forward to growing and learning with you."
    ), parse_mode="Markdown"
    )
    logger.info(f"Приветственное сообщение отправлено пользователю {chat_id}")

    context.job_queue.run_once(ask_city_question, 10, data=chat_id)


async def handle_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатие кнопки 'No' и отправляет напоминание с важностью регистрации"""
    chat_id = update.callback_query.from_user.id
    await context.bot.send_message(
        chat_id=chat_id,
text="🔔 Registration is very important for us to support you better. Please, consider completing it! 📋"
    )
    logger.info(f"Напоминание о важности регистрации отправлено пользователю {chat_id}")

    # Запуск напоминания через 30 секунд
    context.job_queue.run_once(send_followup_message, 20, data=chat_id)

async def send_followup_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение через 30 секунд после напоминания"""
    chat_id = context.job.data
    await context.bot.send_message(
        chat_id=chat_id,
text="✅ Have you completed the registration form? Please select an option below:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅Yes", callback_data="completed_yes")],
            [InlineKeyboardButton("❌No", callback_data="completed_no")]
        ])
    )
    logger.info(f"Отправлено сообщение с вопросом о завершении регистрации пользователю {chat_id}")
