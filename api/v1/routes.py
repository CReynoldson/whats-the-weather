from flask import Blueprint, request as flask_request
import requests

v1_api = Blueprint("v1", __name__, url_prefix="/v1")


@v1_api.route("/weather")
def get_weather():
    city_name = flask_request.args.get("city")
    return "Get ready to start singing (or scowling) in the rain"