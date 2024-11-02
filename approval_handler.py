import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_approval(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Разбор callback_data
    if "_" in query.data:
        action, user_id = query.data.split("_")
        user_id = int(user_id)
    else:
        action = query.data
        user_id = None  # Установим user_id в None, если данные отсутствуют

    if action == "approve" and user_id is not None:
        # Приветственное сообщение
        await context.bot.send_message(
            chat_id=user_id,
            text="We are delighted to have you join our community.\n\n"
            
                 "Please, first take your time and read the Charter of the Public Association KazAELT:\n"
                 "https://drive.google.com/file/d/1pm5uPOFu2Vx_i7VP9QBHmynNvjaB_nSM/view?pli=1",
        )
        logger.info(f"Отправлено приветственное сообщение пользователю {user_id}.")

        # Изменение текста сообщения
        try:
            await query.edit_message_caption(caption="Чек подтвержден. Пользователю отправлено уведомление.")
            logger.info(f"Чек подтвержден. Пользователю отправлено уведомление  для {user_id}.")
        except Exception as e:
            logger.error(f"Ошибка при изменении сообщения: {e}")
        
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
            text="Your check has been rejected. Please contact support or send a new receipt."
        )
        await query.edit_message_caption(caption="Чек отклонен. Пользователю отправлено уведомление.")
        logger.info(f"Чек от пользователя {user_id} отклонён менеджером.")
   

