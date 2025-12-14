"""Точка входа Telegram-бота."""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import BOT_TOKEN, INIT_DATA_PATH
from bot.db import init_db, load_sql_script, is_db_empty
from bot.fortune import get_fortune_lines

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    await message.answer(
        "Напиши название песни, и я подскажу тебе тон дня."
    )


@dp.message(F.text)
async def handle_text(message: Message):
    """Обработчик текстовых сообщений (название песни)."""
    song_title = message.text.strip()
    
    if not song_title:
        await message.answer("Пожалуйста, введите название песни.")
        return
    
    try:
        # Получаем две строки для гадания
        line1, line2 = await get_fortune_lines(song_title)
        
        # Формируем ответ
        response = "Тон дня:\n\n" + line1 + "\n" + line2
        await message.answer(response)
        
    except ValueError as e:
        error_msg = str(e)
        await message.answer(error_msg)
    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {e}", exc_info=True)
        await message.answer("Произошла ошибка. Попробуйте позже.")


async def main():
    """Главная функция запуска бота."""
    # Инициализируем базу данных
    logger.info("Инициализация базы данных...")
    await init_db()
    logger.info("База данных инициализирована")
    
    # Если БД пуста и есть скрипт инициализации - загружаем данные
    if INIT_DATA_PATH and await is_db_empty():
        logger.info("База данных пуста, загружаем начальные данные...")
        try:
            await load_sql_script(INIT_DATA_PATH)
            logger.info("Начальные данные загружены")
        except Exception as e:
            logger.warning(f"Не удалось загрузить начальные данные: {e}")
    
    # Запускаем бота
    logger.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)

