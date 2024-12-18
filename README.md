# Система обработки сообщений с использованием Apache Kafka

## Описание
Проект реализует систему отправки и обработки сообщений о погоде в реальном времени. Применяются Apache Kafka для публикации и отправки сообщений, а также база данных SQLite для хранения собранных данных.

## Пререквизиты
Для работы проекта необходимы:
- **Python 3.8+**
- **Apache Kafka 3.9.0**
- **SQLite**
- **Kafka-python** и **requests** (для Python)
- API-ключ OpenWeatherMap (для получения погодных данных)

## Инструкция по установке и запуску

### 1. Настройка кластера Apache Kafka
1. Скачайте Apache Kafka и распакуйте:
   ```bash
   wget https://dlcdn.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz
   tar -xf kafka_2.13-3.9.0.tgz
   cd kafka_2.13-3.9.0
   ```

2. Запустите **Zookeeper** в отдельном терминале:
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```

3. Запустите Kafka broker в другом терминале:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

4. Создайте топик `weather` с 3 разделами:
   ```bash
   bin/kafka-topics.sh --create --topic weather --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
   ```

5. Проверьте, что топик создан:
   ```bash
   bin/kafka-topics.sh --list --bootstrap-server localhost:9092
   ```

### 2. Настройка продюсера
1. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Установите библиотеки:
   ```bash
   pip install kafka-python requests
   ```

3. Запустите **producer.py**:
   ```bash
   python3 producer.py
   ```
   Продюсер отправляет данные о погоде в топик `weather`.

### 3. Настройка потребителя
1. Запустите **consumer.py**, чтобы считывать данные и сохранять их в SQLite:
   ```bash
   python3 consumer.py
   ```
   Данные будут сохраняться в файл **weather.db**.

### 4. Преобразование в JSON
1. Запустите **convert_weather_db_to_json.py**, чтобы преобразовать SQLite-базу в JSON:
   ```bash
   python3 convert_weather_db_to_json.py
   ```
   Результат: файл **weather.json**, содержащий погодные данные.

## Структура проекта
```
project/
|-- producer.py              # Продюсер данных
|-- consumer.py              # Потребитель и сохранение данных
|-- convert_weather_db_to_json.py   # Конвертация SQLite в JSON
|-- weather.db               # SQLite база
|-- weather.json             # JSON результат
|-- README.md                # Документация
```

## Результаты
- **weather.db**: База данных SQLite, содержащая погодные данные.
- **weather.json**: Конвертированные данные в JSON-формате.