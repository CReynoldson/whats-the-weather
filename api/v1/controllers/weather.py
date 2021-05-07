from app import weather_service
from exceptions.weather import WeatherServiceInvalidParametersException, WeatherServiceControllerException
import logging 

class WeatherHelper():

    # let's make sure no one passes us anything Nefarious™
    # latitude and longitude aren't implemented yet but seem logical additions 
    VALID_ARGUMENTS = ["city", "latitude", "longitude", "unit", "precision"]
    TEMPERATURE_UNITS = ["kelvin", "celsius", "fahrenheit"]
    # temperature-relevant keys to loop through when converting temperature values between units
    TEMPERATURE_KEYS = ["feels_like", "temp", "temp_max", "temp_min"]
      
    def __init__(self, *args):
        try:
            for key in self.VALID_ARGUMENTS:
                
                value = args[0].get(key)
                if not value:
                    continue

                # let users specify 'unit' for ease of use but internally distinguish it from all the base units by calling it temperature_unit
                if key == "unit":
                    if value not in self.TEMPERATURE_UNITS:
                        raise WeatherServiceInvalidParametersException("You've asked for a temperature unit we can't help you with.")
                    self.__setattr__("temperature_unit", value)
                else:
                    self.__setattr__(key, value)
        except IndexError:
            raise IndexError("Cannot initialize Weather Helper with no arguments.")
    
        # OpenWeather uses Kelvin as the standard unit so we shall also do that
        try:
            getattr(self, "temperature_unit")
        except AttributeError:
            self.temperature_unit = "kelvin"

    @classmethod 
    def get_unit_converter(cls, original_unit="kelvin", translation_unit="celsius"):
        """
        :original_unit => string
        :translation_unit => string
        :rtype => method
        Finds the converter class method based on two unit inputs
        """
        try:
            converter = f"{original_unit}_to_{translation_unit}"
            return getattr(cls, converter)
        except AttributeError as e:
            logging.exception(e)
            raise WeatherServiceControllerException(
                "Attempted to locate '{converter}' and failed. If you're seeing this someone forgot to add a unit converter (or maybe they did and just misspelled it)."
            )
        
    @classmethod
    def kelvin_to_celsius(cls, temp):
        """
        :temp => float
        :rtype => float 
        """
        return round(temp - 273.15, 2)
 
    @classmethod
    def kelvin_to_fahrenheit(cls, temp):
        """
        :temp => float
        :rtype => float
        """
        return round((cls.kelvin_to_celsius(temp)) * 9 / 5 + 32, 2)

    @classmethod
    def celsius_to_kelvin(cls, temp):
        raise NotImplementedError
    
    @classmethod
    def celsius_to_fahrenheit(cls, temp):
        raise NotImplementedError
    
    @classmethod
    def fahrenheit_to_kelvin(cls, temp):
        raise NotImplementedError
    
    @classmethod
    def fahrenheit_to_celsius(cls, temp):
        raise NotImplementedError

    def get_weather_for_unit(self, weather, unit):
        """
        :weather => dict of weather data from OpenWeather
        :unit => string identifying the temperature unit we want to convert to

        Determine what temperature unit we received back from OpenWeather (in this example case it will always be Kelvin)
        Convert into the other two types of temperature units
        TODO - opting in to this conversion could be an API parameter, but that's not implemented yet
        """
        unit_converter = self.get_unit_converter(self.temperature_unit, unit)
        unit_weather = {}
        
        for weather_attribute in self.TEMPERATURE_KEYS:
            if weather.get(weather_attribute):
                unit_weather[weather_attribute] = unit_converter(weather[weather_attribute])
        
        return unit_weather 

    def format_response(self, response):
        """
        :response => The json results of our API call to the weather service
        :rtype => dict
        Parses OpenWeather API response and returns only the relevant weather data
        """

        api_weather_data = response["main"]
        pressure = api_weather_data["pressure"]
        humidity = api_weather_data["humidity"]
        weather = {
            "kelvin": api_weather_data,
            "celsius": {
                "pressure": pressure, 
                "humidity": humidity
            },
            "fahrenheit": {
                "pressure": pressure, 
                "humidity": humidity
            }
        }

        for unit in ["celsius", "fahrenheit"]:
            converted_temperatures = self.get_weather_for_unit(api_weather_data, unit)
            weather[unit].update(converted_temperatures)
        
        return {"weather": weather}

    def get_weather(self):
        """
        :rtype => dict
        Calls weather service to proxy API call to OpenWeather
        This would be a great place to add additional query parameter handling if we ever wanted to
        check the weather based on something like latitude or longitude.
        For now, let's just have it validate that we have something to base our query on
        """
        try:
            getattr(self, "city")
        except AttributeError:
            raise WeatherServiceInvalidParametersException("Please provide a city, we simply cannot tell you the weather in a city without a city to check.")
        
        service_response = weather_service.get_weather_by_city_name(self.city)
        return self.format_response(service_response)
