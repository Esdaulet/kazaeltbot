import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на `chat_id` группы, где находятся все менеджеры
group_chat_id = -4595309953  # Замените на реальный chat_id вашей группы

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Разбор callback_data
    if "_" in query.data:
        action, user_id = query.data.split("_")
        user_id = int(user_id)
    else:
        action = query.data
        user_id = None

    if action == "approve" and user_id is not None:
        # Приветственное сообщение пользователю
        await context.bot.send_message(
            chat_id=user_id,
            text="We are delighted to have you join our community.\n\n"
                 "Please, first take your time and read the Charter of the Public Association KazAELT:\n"
                 "https://drive.google.com/file/d/1pm5uPOFu2Vx_i7VP9QBHmynNvjaB_nSM/view?pli=1",
        )
        logger.info(f"Отправлено приветственное сообщение пользователю {user_id}.")

        # Удаляем кнопки у сообщения и обновляем статус в группе
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=None  # Убираем кнопки
            )
            await context.bot.edit_message_caption(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                caption="Чек подтвержден. Пользователю отправлено уведомление."
            )
            logger.info("Кнопки удалены, чек подтвержден в группе.")
        except Exception as e:
            logger.error(f"Ошибка при изменении сообщения в группе: {e}")

        # Отправка уведомления в группу
    

        # Отправка кнопки "I've read"
        await context.bot.send_message(
            chat_id=user_id,
            text="When you are done, please confirm by clicking the button below:",
            reply_markup=InlineKeyboardMarkup([ 
                [InlineKeyboardButton("📖 I've read", callback_data="charter_read")]
            ])
        )
        logger.info(f"Отправлена кнопка 'I've read' пользователю {user_id}.")
    
    elif action == "reject" and user_id is not None:
        await context.bot.send_message(
            chat_id=user_id,
            text="Your check has been rejected. Please send a new receipt."
        )
        # Удаляем кнопки у сообщения и обновляем статус в группе
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup=None  # Убираем кнопки
            )
            await context.bot.edit_message_caption(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                caption="Чек отклонен. Пользователю отправлено уведомление."
            )
            logger.info("Кнопки удалены, чек отклонен в группе.")
        except Exception as e:
            logger.error(f"Ошибка при изменении сообщения в группе: {e}")

        # Отправка уведомления в группу
        await context.bot.send_message(
            chat_id=group_chat_id,
            text="Чек отклонен. Уведомление отправлено пользователю."
        )
