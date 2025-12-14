# Инструкция по деплою бота

## Сохранение базы данных при деплое

База данных сохраняется через Docker volumes. Есть несколько способов обеспечить персистентность данных:

### Способ 1: Локальный volume (для разработки)

В `docker-compose.yml` уже настроен локальный volume:
```yaml
volumes:
  - ./data:/data
```

База данных будет храниться в папке `./data/bot.sqlite3` на хосте.

### Способ 2: Named volume (рекомендуется для продакшена)

Раскомментируйте в `docker-compose.yml`:
```yaml
volumes:
  - bot_data:/data

volumes:
  bot_data:
    driver: local
```

Это создаст именованный volume, который будет сохраняться даже при удалении контейнера.

### Способ 3: Внешний volume (для облачных хостингов)

Для облачных хостингов (DigitalOcean, AWS, etc.) используйте внешние volumes:
```yaml
volumes:
  - /var/lib/fortune-bot/data:/data
```

## Инициализация данных при первом запуске

### Автоматическая загрузка из SQL-скрипта

1. Скопируйте данные из `example_insert.sql` в `init_data.sql`:
   ```bash
   ./init_data_from_example.sh
   ```
   Или вручную:
   ```bash
   cp example_insert.sql init_data.sql
   ```

2. При первом запуске бота, если БД пуста, данные из `init_data.sql` будут автоматически загружены.

3. Файл `init_data.sql` копируется в Docker-образ при сборке.

### Ручная загрузка данных

После запуска контейнера:
```bash
# Войти в контейнер
docker-compose exec bot bash

# Загрузить SQL-скрипт
sqlite3 /data/bot.sqlite3 < /app/example_insert.sql
```

Или с хоста:
```bash
docker-compose exec bot sqlite3 /data/bot.sqlite3 < example_insert.sql
```

### Использование Python-скрипта

```bash
# С хоста (если установлен Python и зависимости)
python add_song.py "Спать с тобой" example_lyrics.txt

# Или из контейнера
docker-compose exec bot python /app/add_song.py "Спать с тобой" /app/example_lyrics.txt
```

## Деплой на хостинг

### 1. Подготовка

1. Создайте `.env` файл с токеном бота:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

2. (Опционально) Подготовьте `init_data.sql` с начальными данными:
   ```bash
   ./init_data_from_example.sh
   ```

### 2. Загрузка на сервер

```bash
# Скопируйте проект на сервер
scp -r . user@server:/path/to/fortune-bot

# Или используйте git
git clone <your-repo> /path/to/fortune-bot
```

### 3. Запуск на сервере

```bash
cd /path/to/fortune-bot

# Соберите и запустите
docker-compose up -d --build

# Проверьте логи
docker-compose logs -f bot
```

### 4. Проверка базы данных

```bash
# Проверить, что БД создана
ls -la data/bot.sqlite3

# Проверить содержимое
docker-compose exec bot sqlite3 /data/bot.sqlite3 "SELECT COUNT(*) FROM tracks;"
```

## Резервное копирование

### Создание бэкапа

```bash
# Создать бэкап БД
cp data/bot.sqlite3 data/bot.sqlite3.backup

# Или через Docker
docker-compose exec bot cp /data/bot.sqlite3 /data/bot.sqlite3.backup
```

### Восстановление из бэкапа

```bash
# Остановить бота
docker-compose down

# Восстановить БД
cp data/bot.sqlite3.backup data/bot.sqlite3

# Запустить бота
docker-compose up -d
```

## Важные замечания

1. **Персистентность данных**: Убедитесь, что volume настроен правильно, иначе данные будут потеряны при перезапуске контейнера.

2. **Права доступа**: Убедитесь, что директория `data/` имеет правильные права:
   ```bash
   chmod 755 data
   ```

3. **Инициализация**: Данные из `init_data.sql` загружаются только при первом запуске, если БД пуста.

4. **Обновление данных**: Для добавления новых песен используйте `add_song.py` или SQL-запросы напрямую.

