class WeatherHelper():

    # let's make sure no one passes us anything Nefarious™
    ARGUMENTS_WHITELIST = ["city", "latitude", "longitude"]

    def __init__(self, *args):
        # figuring out this circular import tomorrow and yes the shame is unbearable thank you for asking
        from services.weather import WeatherService
        self.service = WeatherService()
        for key, value in args[0].items():
            if key in self.ARGUMENTS_WHITELIST:
                self.__setattr__(key, value)

    def format_response(self, response):
        raise NotImplementedError

    def get_weather(self):
        service_response = self.service.get_weather_by_city_name(self.city)
        return self.format_response(service_response)
