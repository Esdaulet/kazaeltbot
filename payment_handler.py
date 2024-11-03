import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ID группы для отправки чеков (замените на реальный ID группы)
group_chat_id = -4595309953  # Замените на реальный ID вашей группы

async def request_payment_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запрашивает PDF-чек при нажатии кнопки 'I have paid'"""
    query = update.callback_query
    await query.answer()
    
    logger.info(f"Пользователь {query.from_user.id} нажал 'I have paid'. Запрашиваем PDF-чек.")
    await query.edit_message_text("Thanks for the payment! Please send the receipt in PDF format.")

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает полученный PDF и отправляет его в группу менеджеров"""
    document = update.message.document
    # Проверяем, что это PDF
    if document and document.mime_type == 'application/pdf':
        logger.info(f"Получен PDF от пользователя {update.message.from_user.id}, отправляем в группу менеджеров.")
        
        caption = f"Receipt from {update.message.from_user.full_name} ({update.message.from_user.id})"
        
        # Клавиатура для одобрения или отклонения
        approval_keyboard = [
            [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{update.message.from_user.id}")],
            [InlineKeyboardButton("❌ Reject", callback_data=f"reject_{update.message.from_user.id}")]
        ]
        approval_reply_markup = InlineKeyboardMarkup(approval_keyboard)

        # Отправляем PDF в группу менеджеров
        try:
            await context.bot.send_document(
                chat_id=group_chat_id,
                document=document.file_id,
                caption=caption,
                reply_markup=approval_reply_markup
            )
            logger.info(f"Чек в формате PDF от пользователя {update.message.from_user.id} отправлен в группу с ID {group_chat_id}.")
        except Exception as e:
            logger.error(f"Ошибка при отправке PDF чека в группу с ID {group_chat_id}: {e}")
        
        await update.message.reply_text("The receipt has been successfully sent to the managers' group for verification. Please wait for an answer.")
    else:
        await update.message.reply_text("Please send the file in PDF format.")
