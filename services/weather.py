import requests
from exceptions.weather import WeatherServiceException, WeatherServiceDownException, WeatherServiceInvalidAPIKeyException, WeatherServiceInvalidParametersException, WeatherServiceRateLimitedException


class WeatherService():
    def __init__(self, token=""):
        if not token:
            raise AttributeError("Cannot initialize Weather Service without an API token.")
        self.api_key = token
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def handle_response(self, response):
        """
        Parses OpenWeather API response
        :rtype => dict or raises exception
        """
        if response.status_code < 400:
            return response.json()
        
        if response.status_code == 401:
            raise WeatherServiceInvalidAPIKeyException("Not able to authenticate with OpenWeather, please check the api token and try again.")
        if response.status_code == 404:
            raise WeatherServiceInvalidParametersException("Attempted to call OpenWeather with invalid parameters, please adjust and try again.")
        if response.status_code == 429:
            raise WeatherServiceRateLimitedException("Wow, you sure want to know about the weather! We've hit our rate limit, please try again in a minute.")
        if response.status_code >= 500:
            raise WeatherServiceDownException("OpenWeather is having some issues and we can't get ahold of them. Please try again later.")
        # something not listed in OpenWeather's documentation has gone awry, let's raise the error with what they told us was the problem
        raise WeatherServiceException(response.json()["message"])
        

    def get_weather_by_city_name(self, city_name):
        """
        OpenWeather API caller that only knows how to handle city names at the moment, thus the very granular method name.
        Could be refactored to be more generic and build its own query string, or we could build out other methods to check 
        for other query parameters, such as get_weather_by_lat_long or get_weather_by_guesstimating_how_fast_the_clouds_are_moving.
        :city_name => string
        :rtype => dict
        """
        query_parameters = ({"appid": self.api_key, "q": city_name})
        response = self.handle_response(requests.get(self.base_url, params=query_parameters))
        return response