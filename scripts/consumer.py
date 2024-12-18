# consumer.py
from kafka import KafkaConsumer
import json
import sqlite3

consumer = KafkaConsumer(
    'weather',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='weather-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Подключение к базе данных SQLite
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Создание таблицы, если ее нет
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        condition TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

print("Ожидание сообщений...")

for message in consumer:
    data = message.value
    cursor.execute('''
        INSERT INTO weather (city, temperature, condition)
        VALUES (?, ?, ?)
    ''', (data['city'], data['temperature'], data['condition']))
    conn.commit()
    print(f"Получено и сохранено сообщение: {data}")
