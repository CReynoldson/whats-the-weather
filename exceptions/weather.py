class WeatherServiceException(Exception):
    status_code = 403

class WeatherServiceDownException(WeatherServiceException):
    status_code = 500 

class WeatherServiceInvalidParametersException(WeatherServiceException):
    status_code = 403 

class WeatherServiceInvalidAPIKeyException(WeatherServiceException):
    status_code = 401

class WeatherServiceRateLimitedException(WeatherServiceException):
    status_code = 429