"""Логика нормализации и гадания на строках песен."""
import random
import re
from typing import List, Tuple

from bot.db import find_track_by_normalized_title, get_track_lines


def normalize_title(title: str) -> str:
    """
    Нормализация названия песни:
    - lower()
    - trim
    - замена ё → е
    - удаление лишних пробелов
    
    Args:
        title: Исходное название
        
    Returns:
        Нормализованное название
    """
    # Приводим к нижнему регистру
    normalized = title.lower()
    
    # Заменяем ё на е
    normalized = normalized.replace("ё", "е")
    
    # Удаляем лишние пробелы (заменяем множественные пробелы на один)
    normalized = re.sub(r"\s+", " ", normalized)
    
    # Trim (удаляем пробелы в начале и конце)
    normalized = normalized.strip()
    
    return normalized


async def get_fortune_lines(song_title: str) -> Tuple[str, str]:
    """
    Получить две случайные строки из песни для гадания.
    
    Args:
        song_title: Название песни от пользователя
        
    Returns:
        Кортеж из двух строк
        
    Raises:
        ValueError: Если песня не найдена или недостаточно данных
    """
    # Нормализуем название
    normalized = normalize_title(song_title)
    
    # Ищем трек в БД
    track_id = await find_track_by_normalized_title(normalized)
    
    if track_id is None:
        raise ValueError("песня не найдена")
    
    # Получаем все строки трека
    lines = await get_track_lines(track_id)
    
    # Фильтруем пустые строки
    non_empty_lines = [(line_no, text) for line_no, text in lines if text.strip()]
    
    if len(non_empty_lines) < 2:
        raise ValueError("недостаточно данных")
    
    # Находим все пары подряд идущих строк
    # Ищем line_no, у которого существует line_no + 1
    consecutive_pairs = []
    line_nos = {line_no for line_no, _ in non_empty_lines}
    
    for line_no, text in non_empty_lines:
        if (line_no + 1) in line_nos:
            # Находим следующую строку
            next_line = next((t for l, t in non_empty_lines if l == line_no + 1), None)
            if next_line:
                consecutive_pairs.append((text, next_line))
    
    if not consecutive_pairs:
        raise ValueError("недостаточно данных")
    
    # Выбираем случайную пару
    line1, line2 = random.choice(consecutive_pairs)
    
    return line1, line2

