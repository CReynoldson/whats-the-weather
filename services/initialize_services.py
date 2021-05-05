from app import app 
from services.weather import WeatherService 

def get_weather_service():
    return WeatherService(token=app.config.get("WEATHER_SERVICE_API_KEY"))