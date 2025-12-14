#!/bin/bash
# Скрипт для копирования данных из example_insert.sql в init_data.sql
# Использование: ./init_data_from_example.sh

if [ -f "example_insert.sql" ]; then
    cp example_insert.sql init_data.sql
    echo "Данные из example_insert.sql скопированы в init_data.sql"
    echo "Теперь при первом запуске бота эти данные будут автоматически загружены"
else
    echo "Файл example_insert.sql не найден"
    exit 1
fi

