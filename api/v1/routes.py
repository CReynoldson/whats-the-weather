from flask import Blueprint, request, jsonify
from api.v1.controllers.weather import WeatherHelper
from exceptions.weather import WeatherServiceException

v1_api = Blueprint("v1", __name__, url_prefix="/v1")


@v1_api.route("/weather")
def get_weather():
    city_name = request.args.get("city")
    query_parameters = request.args
    helper = WeatherHelper(query_parameters)
    try:
        return jsonify({"results": "success", "data": helper.get_weather()}), 200
    except WeatherServiceException as e:
        return jsonify({"results": "failure", "message": e.args[0]}), e.status_code