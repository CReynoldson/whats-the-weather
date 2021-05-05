class WeatherServiceException(Exception):
    pass 

class WeatherServiceDownException(WeatherServiceException):
    pass 

class WeatherServiceInvalidParametersException(WeatherServiceException):
    pass 

class WeatherServiceInvalidAPIKeyException(WeatherServiceException):
    pass

class WeatherServiceRateLimitedException(WeatherServiceException):
    pass