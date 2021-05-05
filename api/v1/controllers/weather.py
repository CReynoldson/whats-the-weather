from app import weather_service
from exceptions.weather import WeatherServiceInvalidParametersException

class WeatherHelper():

    # let's make sure no one passes us anything Nefarious™
    # latitude and longitude aren't implemented yet but seem logical additions 
    ARGUMENTS_WHITELIST = ["city", "latitude", "longitude"]

    def __init__(self, *args):
        for key, value in args[0].items():
            if key in self.ARGUMENTS_WHITELIST:
                self.__setattr__(key, value)

    def format_response(self, response):
        """
        Parses OpenWeather API response and returns only the relevant weather data
        :response => The json results of our API call to the weather service
        :rtype => dict
        """
        weather_data = {
            "weather": response["main"]
        }
        return weather_data

    def get_weather(self):
        """
        Calls weather service to proxy API call to OpenWeather
        This would be a great place to add additional query parameter handling if we ever wanted to
        check the weather based on something like latitude or longitude.
        For now, let's just have it validate that we have something to base our query on
        :rtype => dict
        """
        if not self.city:
            raise WeatherServiceInvalidParametersException("Please provide a city, we simply cannot tell you the weather in a city without a city to check")
        service_response = weather_service.get_weather_by_city_name(self.city)
        return self.format_response(service_response)
