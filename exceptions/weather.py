class WeatherServiceException(Exception):
    status_code = 400

class WeatherServiceDownException(WeatherServiceException):
    status_code = 500 

class WeatherServiceInvalidParametersException(WeatherServiceException):
    status_code = 400 

class WeatherServiceInvalidAPIKeyException(WeatherServiceException):
    status_code = 401

class WeatherServiceRateLimitedException(WeatherServiceException):
    status_code = 429

class WeatherServiceControllerException(WeatherServiceException):
    """
    Use internally to flag coding errors or potential data mismanagement
    """
    status_code = 500
