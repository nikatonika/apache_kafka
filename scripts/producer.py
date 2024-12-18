# producer.py
import json
import time
import requests
from kafka import KafkaProducer

# Ваш API ключ от OpenWeatherMap
API_KEY = '512776928940447652f346921a7f6900'

# Список городов
cities = ["Москва", "Санкт-Петербург", "Красноярск", "Сочи", "Владивосток"]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_weather_data(city):
    # Параметры запроса
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',  # Используем метрическую систему (градусы Цельсия)
        'lang': 'ru'        # Локализация на русский язык
    }

    # URL для запроса текущей погоды
    url = 'http://api.openweathermap.org/data/2.5/weather'

    try:

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'condition': data['weather'][0]['description']
            }
            return weather_data
        else:
            print(f"Ошибка получения данных для города {city}: {data['message']}")
            return None
    except Exception as e:
        print(f"Исключение при получении данных для города {city}: {e}")
        return None

if __name__ == "__main__":
    while True:
        for city in cities:
            weather_data = get_weather_data(city)
            if weather_data:
                producer.send('weather', weather_data)
                print(f"Отправлены данные: {weather_data}")
            time.sleep(1)  # Небольшая пауза между запросами
        time.sleep(300)  # Пауза перед следующим циклом (5 минут)

