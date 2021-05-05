import json
from flask import Flask 
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

from services.initialize_services import get_weather_service
weather_service = get_weather_service()

from api.v1.routes import v1_api
app.register_blueprint(v1_api)
