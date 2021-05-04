from app import app
import requests

class WeatherService():
    def __init__(self):
        self.api_key = app.config.get("WEATHER_SERVICE_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def handle_response(self, response):
        # TODO - actual handling
        return response

    def get_weather_by_city_name(self, city_name):
        query_parameters = ({"appid": self.api_key, "q": city_name})
        response = self.handle_response(requests.get(self.base_url, params=query_parameters))
        return response