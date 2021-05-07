import os 
class Config(object):
    WEATHER_SERVICE_API_KEY = os.environ["WEATHER_SERVICE_API_KEY"]
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")