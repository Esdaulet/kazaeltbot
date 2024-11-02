import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Настройка логгирования
logger = logging.getLogger(__name__)

# Словарь городов и их ссылок
city_links = {
    "Toleby region": "https://chat.whatsapp.com/BGRjzrsQQWm78T3lMA3xoi",
    "Karaganda": "https://chat.whatsapp.com/EgekmRS49bk2BPHLN6zHpX",
    "Uralsk": "https://chat.whatsapp.com/IilYyzdCJkD5XUWtBMQMJI",
    "Taraz": "https://chat.whatsapp.com/IqgckyPVYzh1B4O6muAq3h",
    "Zhanaozen": "https://chat.whatsapp.com/Ew6hBEgEvMo3miUv8VoLmQ",
    "Astana": "https://chat.whatsapp.com/FdqCM5VfKgE52v8GzaQWn8",
    "Oskemen, Ridder": "https://chat.whatsapp.com/EYCGk9TqxN34lFPYAf6kUz",
    "Almaty region": "https://chat.whatsapp.com/DvJkZDom9LwBnacTcgMP08",
    "Almaty": "https://chat.whatsapp.com/KOA0OS9Ho9jAgL7bHFHAlc",
    "Turkistan region": "https://chat.whatsapp.com/D8cbiHWAytn6WHlwXfcAlP",
    "Semey": "https://chat.whatsapp.com/CCWq71tiw6BL8ftQ8qys3a",
    "Shymkent": "https://chat.whatsapp.com/F41nVHCdfsdIwYpops0hvy", 
    "North KZ region": "https://chat.whatsapp.com/DYgzTXi5BNNCRh2QvEv8Nt", 
    "Kyzylorda": "https://chat.whatsapp.com/F8I6KOXEc7FE5ul92j7jvJ", 
    "Pavlodar": "https://chat.whatsapp.com/HlsMqRy2ZFC33a4lceJKih", 
    "Aktau": "https://chat.whatsapp.com/Igr0WUdAboL9AqDwFQxR8H",
    "Kokshetau": "https://chat.whatsapp.com/EnDib0lPL0vJ5IkryC7ozu",
    "Aktobe": "https://chat.whatsapp.com/Gk29lcUxLxNKjhWSrjYvpO",
    "Atyrau": "https://chat.whatsapp.com/CRPRjeB9ADT2sCiERad4t4",
    "Kostanay": "https://chat.whatsapp.com/L68Pb2VBGsX81EzIpQqHCn",
    "Taldykorgan": "https://chat.whatsapp.com/FvGbBlU5fFG7B7PI0TtWFT",
    "Kazgurt": "https://chat.whatsapp.com/Db72ovk8Y9BHfuVXHvdsSR",
    # Добавьте остальные города и ссылки
}

async def ask_city_question(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет вопрос о городе и кнопки с названиями городов"""
    chat_id = context.job.data

    # Создание кнопок с названиями городов
    keyboard = [
        [InlineKeyboardButton(city, callback_data=city) for city in list(city_links.keys())[i:i+3]]
        for i in range(0, len(city_links), 3)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправка вопроса о городе с клавиатурой кнопок
    await context.bot.send_message(
        chat_id=chat_id,
        text="By the way, which city are you from? Please select from the options below:",
        reply_markup=reply_markup
    )
    logger.info(f"Вопрос о городе отправлен пользователю {chat_id}")

async def handle_city_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает выбор города и отправляет соответствующую ссылку"""
    query = update.callback_query
    await query.answer()
    selected_city = query.data

    # Получение ссылки для выбранного города
    if selected_city in city_links:
        link = city_links[selected_city]
        await context.bot.send_message(
            chat_id=query.from_user.id,
        text=f"🌍 Here is the link for {selected_city}: {link}\n\nYou can join the chat for your city to stay connected and informed!"
        )
        logger.info(f"Ссылка для {selected_city} отправлена пользователю {query.from_user.id}")
    else:
        logger.error(f"Неизвестный город: {selected_city}")
