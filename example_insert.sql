-- Пример добавления песни "Спать с тобой" в базу данных
-- Использование: sqlite3 /data/bot.sqlite3 < example_insert.sql

-- Добавляем трек
-- Нормализованное название: "спать с тобой" (lower, trim, ё→е)
INSERT INTO tracks (title, normalized_title) 
VALUES ('Спать с тобой', 'спать с тобой');

-- Получаем ID только что добавленного трека
-- (В SQLite это можно сделать через last_insert_rowid(), но для примера используем явный запрос)
-- Предположим, что ID = (SELECT id FROM tracks WHERE title = 'Спать с тобой')

-- Добавляем строки песни
-- Важно: line_no должны быть последовательными для корректной работы логики гадания

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    1,
    'А как же…';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    2,
    'Ёб твою мать, я люблю твои волосы';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    3,
    'Я хочу спать с тобой, я хочу стать тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    4,
    'Чтобы спать самой с собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    5,
    'Чтобы хотя бы так спать с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    6,
    'Или другому типу с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    7,
    'Или вообще никому с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    8,
    'Запутался, не пойму ничего';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    9,
    'Просто я пробую…';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    10,
    'Спать с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    11,
    'Нахуй твой зефир в кровать';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    12,
    'Ты собираешься дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    13,
    'Облако в моих штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    14,
    'Я собираюсь дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    15,
    'Облако в твоих штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    16,
    'А может быть, я под кислотой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    17,
    'И у меня галлюцинации и всё такое';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    18,
    'Спать с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    19,
    'Нахуй твой зефир в кровать';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    20,
    'Ты собираешься дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    21,
    'Облако в моих штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    22,
    'Я собираюсь дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    23,
    'Облако в твоих штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    24,
    'А может быть, я под кислотой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    25,
    'И у меня галлюцинации и всё такое';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    26,
    'Спать с тобой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    27,
    'Зефир в кровать';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    28,
    'Дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    29,
    'В штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    30,
    'Дополнять';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    31,
    'В штанах собой';

INSERT INTO lines (track_id, line_no, text) 
SELECT 
    (SELECT id FROM tracks WHERE title = 'Спать с тобой'),
    32,
    'Кислотой';

