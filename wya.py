#!/usr/bin/env python3
import requests
import json

API_URL = "https://api.weather.yandex.ru/graphql/query"
API_KEY = "demo_yandex_weather_api_key_ca6d09349ba0"  # Замените на свой ключ
LATITUDE = 55.030199
LONGITUDE = 82.92043

WEATHER_ICONS = {
    "CLEAR": "",  # ☀️
    "PARTLY_CLOUDY": "",  # 🌤
    "CLOUDY": "",  # ☁️
    "OVERCAST": "",  # 🌥
    "LIGHT_RAIN": "",  # 🌦
    "RAIN": "",  # 🌧
    "HEAVY_RAIN": "",  # 🌩
    "SHOWERS": "",  # 🌧
    "SLEET": "󱋋",  # 🌨
    "LIGHT_SNOW": "󰜗",  # 🌨
    "SNOW": "󰜗",  # ❄️
    "SNOWFALL": "󰜗󰜗",  # 🌨
    "HAIL": "󰖒",  # 🌩
    "THUNDERSTORM": "󱐋",  # ⛈
    "THUNDERSTORM_WITH_RAIN": "󱐋󰖗",  # 🌩
    "THUNDERSTORM_WITH_HAIL": "󱐋󰖒",  # 🌩
}

WIND_ICONS = {
    "NORTH": "󱦲",
    "NORTH_EAST": "󱦴",
    "EAST": "󰁔",
    "SOUTH_EAST": "󱦷",
    "SOUTH": "󱦳",
    "SOUTH_WEST": "󱦶",
    "WEST": "󱦱",
    "NORTH_WEST": "󱦵",
    "CALM": " ",
}

CONDITION_TRANSLATION = {
    "CLEAR": "Ясно",
    "PARTLY_CLOUDY": "Малооблачно",
    "CLOUDY": "Облачно",
    "OVERCAST": "Пасмурно",
    "LIGHT_RAIN": "Небольшой дождь",
    "RAIN": "Дождь",
    "HEAVY_RAIN": "Сильный дождь",
    "SHOWERS": "Ливень",
    "SLEET": "Дождь со снегом",
    "LIGHT_SNOW": "Небольшой снег",
    "SNOW": "Снег",
    "SNOWFALL": "Снегопад",
    "HAIL": "Град",
    "THUNDERSTORM": "Гроза",
    "THUNDERSTORM_WITH_RAIN": "Гроза с дождем",
    "THUNDERSTORM_WITH_HAIL": "Гроза с градом",
}


def fetch_weather():
    query = {
        "query": f'''
        {{
            weatherByPoint(request: {{ lat: {LATITUDE}, lon: {LONGITUDE} }}) {{
                now {{
                    temperature
                    windSpeed
                    windDirection
                    condition
                }}
            }}
        }}
        '''
    }

    headers = {
        "x-yandex-weather-key": API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=query)
    return response.json()

def get_weather_data():
    data = fetch_weather()["data"]["weatherByPoint"]["now"]
    
    temperature = data["temperature"]
    condition = data["condition"]
    wind_speed = data["windSpeed"]
    wind_direction = data["windDirection"]

    return temperature, condition, wind_speed, wind_direction

def format_weather():
    temperature, condition, wind_speed, wind_direction = get_weather_data()

    weather_icon = WEATHER_ICONS.get(condition, "?")
    wind_icon = WIND_ICONS.get(wind_direction, "?")
   
    condition_translate = CONDITION_TRANSLATION.get(condition, condition.capitalize())


    text = f"{weather_icon} {temperature}°C"
    tooltip = f"{condition_translate}, {temperature}°C\n" \
              f"Ветер: {wind_speed} м/с {wind_icon}"
    
    return {
        "text": text,
        "tooltip": tooltip,
        "class": "normal"
    }

if __name__ == "__main__":
    weather = format_weather()
    print(json.dumps(weather))

