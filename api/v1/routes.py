from flask import Blueprint, request
from .controllers.weather import WeatherHelper

v1_api = Blueprint("v1", __name__, url_prefix="/v1")


@v1_api.route("/weather")
def get_weather():
    city_name = request.args.get("city")
    query_parameters = request.args
    helper = WeatherHelper(query_parameters)
    helper.get_weather()
    return "Get ready to start singing (or scowling) in the rain"