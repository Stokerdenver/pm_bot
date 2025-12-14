"""Работа с базой данных SQLite через aiosqlite."""
import aiosqlite
from pathlib import Path
from typing import Optional, List, Tuple

from bot.config import DB_PATH


async def init_db() -> None:
    """Инициализация базы данных: создание таблиц, если их нет."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Создаем таблицу tracks
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                title TEXT UNIQUE NOT NULL,
                normalized_title TEXT NOT NULL
            )
        """)
        
        # Создаем таблицу lines
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lines (
                id INTEGER PRIMARY KEY,
                track_id INTEGER NOT NULL,
                line_no INTEGER NOT NULL,
                text TEXT NOT NULL,
                FOREIGN KEY(track_id) REFERENCES tracks(id)
            )
        """)
        
        # Создаем индексы для ускорения поиска
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_tracks_normalized 
            ON tracks(normalized_title)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_lines_track_id 
            ON lines(track_id)
        """)
        
        await db.commit()


async def load_sql_script(script_path: str) -> None:
    """
    Загрузить и выполнить SQL-скрипт.
    
    Args:
        script_path: Путь к SQL-скрипту
    """
    script_file = Path(script_path)
    if not script_file.exists():
        return
    
    async with aiosqlite.connect(DB_PATH) as db:
        # Читаем SQL-скрипт
        sql_content = script_file.read_text(encoding='utf-8')
        
        # Удаляем комментарии (строки, начинающиеся с --)
        lines = []
        for line in sql_content.split('\n'):
            # Удаляем комментарии из строки
            comment_pos = line.find('--')
            if comment_pos != -1:
                line = line[:comment_pos]
            line = line.strip()
            if line:
                lines.append(line)
        
        # Объединяем строки и разделяем по ;
        full_sql = ' '.join(lines)
        
        # Разделяем по ; для выполнения отдельных команд
        statements = [s.strip() for s in full_sql.split(';') if s.strip()]
        
        for statement in statements:
            if statement:
                await db.execute(statement)
        
        await db.commit()


async def is_db_empty() -> bool:
    """
    Проверить, пуста ли база данных.
    
    Returns:
        True, если в БД нет треков
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) as count FROM tracks") as cursor:
            row = await cursor.fetchone()
            return row[0] == 0 if row else True


async def find_track_by_normalized_title(normalized_title: str) -> Optional[int]:
    """
    Поиск трека по нормализованному названию.
    
    Args:
        normalized_title: Нормализованное название песни
        
    Returns:
        ID трека или None, если не найден
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id FROM tracks WHERE normalized_title LIKE ? LIMIT 1",
            (f"%{normalized_title}%",)
        ) as cursor:
            row = await cursor.fetchone()
            return row["id"] if row else None


async def get_track_lines(track_id: int) -> List[Tuple[int, str]]:
    """
    Получить все строки трека (line_no, text).
    
    Args:
        track_id: ID трека
        
    Returns:
        Список кортежей (line_no, text)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT line_no, text FROM lines WHERE track_id = ? ORDER BY line_no",
            (track_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [(row["line_no"], row["text"]) for row in rows]
