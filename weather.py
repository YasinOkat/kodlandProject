from dataclasses import dataclass
import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')


@dataclass
class WeatherData:
    icon: str
    max_temp: int
    min_temp: int


def get_current_weather(cityName, API_key):
    resp = requests.get(
        f'http://api.weatherapi.com/v1/forecast.json?key={API_key}&q={cityName}&days=3&aqi=no&alerts=no').json()

    forecast_days = resp['forecast']['forecastday']

    # Extract forecast data for the first day
    day1 = forecast_days[0]['day']
    day1_data = WeatherData(
        icon=day1['condition']['icon'],
        max_temp=day1['maxtemp_c'],
        min_temp=day1['mintemp_c']
    )

    day2 = forecast_days[1]['day']
    day2_data = WeatherData(
        icon=day2['condition']['icon'],
        max_temp=day2['maxtemp_c'],
        min_temp=day2['mintemp_c']
    )

    day3 = forecast_days[2]['day']
    day3_data = WeatherData(
        icon=day3['condition']['icon'],
        max_temp=day3['maxtemp_c'],
        min_temp=day3['mintemp_c']
    )

    current_date = datetime.datetime.now()

    day_of_week = current_date.weekday()

    day_names = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

    day1_name = day_names[day_of_week]
    day2_name = day_names[(day_of_week + 1) % 7]
    day3_name = day_names[(day_of_week + 2) % 7]

    return day1_data, day2_data, day3_data, day1_name, day2_name, day3_name


def main(city):
    city = city.translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU"))

    weather_data = get_current_weather(city, api_key)
    return weather_data


if __name__ == "__main__":
    weather_data = get_current_weather('Ankara', api_key)
    print(get_current_weather('Ankara', api_key))
