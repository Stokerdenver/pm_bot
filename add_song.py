#!/usr/bin/env python3
"""
Скрипт для добавления песен в базу данных.
Пример использования:
    python add_song.py "Спать с тобой" lyrics.txt
"""
import asyncio
import sys
from pathlib import Path
from typing import List

import aiosqlite

from bot.config import DB_PATH
from bot.fortune import normalize_title


async def add_song(title: str, lines: List[str]) -> None:
    """
    Добавить песню в базу данных.
    
    Args:
        title: Название песни
        lines: Список строк песни (без пустых строк)
    """
    normalized = normalize_title(title)
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, существует ли уже такая песня
        async with db.execute(
            "SELECT id FROM tracks WHERE normalized_title = ?",
            (normalized,)
        ) as cursor:
            existing = await cursor.fetchone()
            if existing:
                print(f"Песня '{title}' уже существует в базе (ID: {existing[0]})")
                return
        
        # Добавляем трек
        cursor = await db.execute(
            "INSERT INTO tracks (title, normalized_title) VALUES (?, ?)",
            (title, normalized)
        )
        track_id = cursor.lastrowid
        print(f"Добавлен трек: {title} (ID: {track_id}, normalized: {normalized})")
        
        # Фильтруем пустые строки и добавляем их в БД
        line_no = 1
        added_count = 0
        for line in lines:
            line = line.strip()
            if line:  # Пропускаем пустые строки
                await db.execute(
                    "INSERT INTO lines (track_id, line_no, text) VALUES (?, ?, ?)",
                    (track_id, line_no, line)
                )
                line_no += 1
                added_count += 1
        
        await db.commit()
        print(f"Добавлено строк: {added_count}")


async def add_song_from_text(title: str, text: str) -> None:
    """
    Добавить песню из текста (разбивает на строки).
    
    Args:
        title: Название песни
        text: Текст песни (с переносами строк)
    """
    # Разбиваем на строки и фильтруем пустые
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    # Удаляем метки типа [Интро], [Куплет] и т.д.
    lines = [line for line in lines if not (line.startswith('[') and line.endswith(']'))]
    await add_song(title, lines)


async def main():
    """Главная функция."""
    if len(sys.argv) < 2:
        print("Использование: python add_song.py <название> [файл_с_текстом]")
        print("\nПример:")
        print('  python add_song.py "Спать с тобой" lyrics.txt')
        print("\nИли интерактивный режим:")
        print('  python add_song.py "Спать с тобой"')
        sys.exit(1)
    
    title = sys.argv[1]
    
    if len(sys.argv) >= 3:
        # Читаем из файла
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"Файл не найден: {file_path}")
            sys.exit(1)
        text = file_path.read_text(encoding='utf-8')
        await add_song_from_text(title, text)
    else:
        # Интерактивный режим - читаем из stdin
        print(f"Введите текст песни '{title}' (Ctrl+D для завершения):")
        text = sys.stdin.read()
        await add_song_from_text(title, text)


if __name__ == "__main__":
    asyncio.run(main())

