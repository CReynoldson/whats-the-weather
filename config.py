import os 
class Config():
    DEFAULT_SETTINGS = {
        "WEATHER_SERVICE_API_KEY": os.environ["WEATHER_SERVICE_API_KEY"]
    }