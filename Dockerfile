FROM python:3.12-slim

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY bot/ ./bot/

# Копируем скрипт для добавления песен
COPY add_song.py ./

# Копируем SQL-скрипты для инициализации (если есть)
COPY init_data.sql* ./

# Запускаем бота
CMD ["python", "-m", "bot.app"]

