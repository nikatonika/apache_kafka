import sqlite3
import json

# Укажите путь к вашему файлу базы данных
database_file = 'weather.db'

# Подключаемся к базе данных
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Получаем список всех таблиц в базе данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Инициализируем словарь для хранения данных из всех таблиц
db_data = {}

for table in tables:
    table_name = table[0]
    # Получаем все данные из таблицы
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Получаем имена столбцов
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]

    # Создаем список словарей, где каждый словарь представляет строку данных
    table_data = []
    for row in rows:
        row_data = dict(zip(column_names, row))
        table_data.append(row_data)

    # Добавляем данные таблицы в общий словарь
    db_data[table_name] = table_data

# Закрываем соединение с базой данных
conn.close()

# Записываем данные в файл JSON
json_file = 'weather.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(db_data, f, ensure_ascii=False, indent=4)

print(f"Данные успешно сохранены в файл {json_file}")
