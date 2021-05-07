import flask
import unittest
import pytest 
from app import app, weather_service
from api.v1.controllers.weather import WeatherHelper
from services.weather import WeatherService
from exceptions.weather import WeatherServiceInvalidAPIKeyException, WeatherServiceInvalidParametersException

API_TOKEN = app.config.get("API_TOKEN")

class TestWeatherAPI(unittest.TestCase):
    def test_route_failure_cases(self):
        with app.test_client() as client:
            with app.app_context():
                # v2 of the API isn't implemented yet, stay tuned
                response = client.get("/v2/weather")
                # assert response.status_code == 404
                self.assertEqual(response.status_code, 404)

                # we only allow get requests to /v1/weather, 
                # so anything else should throw a 405 - method not allowed
                response = client.post("/v1/weather")
                self.assertEqual(response.status_code, 405)

                response = client.put("/v1/weather")
                self.assertEqual(response.status_code, 405)

                response = client.delete("/v1/weather")
                self.assertEqual(response.status_code, 405)

                # if you do use the right method, you need an authentication token
                response = client.get("/v1/weather?city=Penticton")
                self.assertEqual(response.status_code, 401)

    def test_controller_failure_cases(self):
        with app.test_client() as client:
            with app.app_context():
                # initialize the helper without any parameters
                # this should raise an IndexError when we try to unpack the arguments in __init__
                with self.assertRaises(IndexError):
                    helper = WeatherHelper()

                # initialize the helper with unhelpful parameters
                # this should raise a custom exception asking for a city
                helper = WeatherHelper({"latitude": 2})
                with self.assertRaises(WeatherServiceInvalidParametersException):
                    helper.get_weather()
    
    def test_service_failure_cases(self):
        with app.test_client() as client:
            with app.app_context():
                # can't initialize without an API token
                with self.assertRaises(AttributeError):
                    service = WeatherService()
                
                # trying to make a call with a bad token returns an error
                with self.assertRaises(WeatherServiceInvalidAPIKeyException):
                    service = WeatherService("WhoRemembersThatMovieNicholasCageWasInCalledTheWeatherman?I'veBeenThinkingAboutItALotWhileDoingThisProject")
                    service.get_weather_by_city_name("Victoria")

                # trying to make a call with the right token but a nonexistent city returns an error
                # we know it's the right token because we're using the service instantiated within the app, which has the right config
                with self.assertRaises(WeatherServiceInvalidParametersException):
                    weather_service.get_weather_by_city_name("Welcome to Hamunaptra; don't read any books!")

    def test_service_success_case(self):
        with app.test_client() as client:
            with app.app_context():
                # if this fails it raises an error and if it succeeds we get a dictionary back
                response = weather_service.get_weather_by_city_name("Vancouver")
                self.assertIsInstance(response, dict) 
    
    def test_controller_success_case(self):
        with app.test_client() as client:
            with app.app_context():
                # if this fails it raises an error and if it succeeds we get a dictionary back
                helper = WeatherHelper({"city": "Merritt"})
                response = helper.get_weather()
                self.assertIsInstance(response, dict) 

    def test_controller_temperature_unit_cases(self):
        with app.test_client() as client:
            with app.app_context():
                # if we initialize the controller without a unit argument, it should default the 'temperature_unit' instance variable to kelvin
                helper = WeatherHelper({"city": "Dublin"})
                self.assertEqual(helper.temperature_unit, "kelvin")
                
                # if we initialize the controller with a unit argument, we should see it set as an instance variable called 'temperature_unit'
                helper = WeatherHelper({"city": "Dublin", "unit": "celsius"}) # you can also run this with fahrenheit but I refuse to give in to manifest destiny
                self.assertEqual(helper.temperature_unit, "celsius")

                # attempting to initialize the controller with an invalid unit argument throws an error
                with self.assertRaises(WeatherServiceInvalidParametersException):
                    helper = WeatherHelper({"city": "Coeur de Coeur", "unit": "I will name a dog Digby one day and I will have #NoRagrets about it"})


    def test_route_success_case(self):
        with app.test_client() as client:
            with app.app_context():
                response = client.get(
                    f"/v1/weather?city=Halifax&app-token={API_TOKEN}")
                response = response.json
                self.assertEqual(response["results"], "success")
                self.assertIn("data", response)
                self.assertIn("weather", response["data"])
