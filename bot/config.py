"""Конфигурация бота."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в переменных окружения")

# Путь к базе данных
DB_PATH = os.getenv("DB_PATH", "/data/bot.sqlite3")

# Путь к SQL-скрипту для инициализации данных (опционально)
# По умолчанию: /app/init_data.sql
# Чтобы отключить: установите INIT_DATA_PATH="" в .env
init_data_path = os.getenv("INIT_DATA_PATH", "/app/init_data.sql")
INIT_DATA_PATH = init_data_path if init_data_path else None

# Создаем директорию для БД, если её нет
db_dir = Path(DB_PATH).parent
db_dir.mkdir(parents=True, exist_ok=True)

