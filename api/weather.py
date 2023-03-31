from flask import jsonify
import requests
from datetime import datetime, timedelta

class Weather:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.weather_url = 'https://api.openweathermap.org/data/2.5/weather'
        self.forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'

    def get_current_weather(self, location: str):
        # make a request to the OpenWeatherMap API
        url = f'{self.weather_url}?q={location}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        # parse the response and extract relevant weather information
        if data['cod'] != 200:
            return jsonify({'error': data['message']}), data['cod']

        current_temp = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']

        # construct the response object with the weather data and forecast
        response_data = {
            'location': location,
            'current_weather': {
                'temperature': current_temp,
                'humidity': humidity,
                'weather_description': weather_description,
                'icon_code': icon_code
            },
        }

        return jsonify(response_data)

    def get_forecast(self, location: str):
        # make a request to the OpenWeatherMap API for the forecast
        url = f'{self.forecast_url}?q={location}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        # parse the response and extract the forecast information per day
        forecasts = {} 
        for item in data['list']:
            dt = datetime.fromisoformat(item['dt_txt'])
            date = dt.date().strftime('%Y-%m-%d')
            if date not in forecasts:
                forecasts[date] = {
                    'datetime': dt.isoformat(),
                    'temp': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'weather_description': item['weather'][0]['description'],
                    'icon_code': item['weather'][0]['icon']
                }

        response_data = {
            'location': location,
            'forecast': forecasts
        }
        return jsonify(response_data)