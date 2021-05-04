from flask import Flask 
from config import Config
from api.v1.routes import v1_api
# from services.weather import WeatherService

app = Flask(__name__)

app.config.from_object(Config.DEFAULT_SETTINGS)

# weather_service = WeatherService(app.config.get("WEATHER_SERVICE_API_KEY"))

app.register_blueprint(v1_api)
