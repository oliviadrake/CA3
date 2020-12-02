''' gets information from a weather api and returns relevant data '''

import requests
from config_file import return_weather_api_key, return_weather_url, return_local_location


def get_weather():
    ''' Reads the weather from an API

        Returns 4 variables describing the location, weather description,
        and temperatures in a dictionary format'''

    api_key = return_weather_api_key()
    location = return_local_location()

    base_url = return_weather_url()
    complete_url = base_url + "appid=" + api_key + "&q=" + location
    response = requests.get(complete_url)

    json_response = response.json()
    main = json_response["main"]

    air_temperature_kelvin = main["temp"]
    feels_like_temperature_kelvin = main["feels_like"]
    location_name = json_response["name"]
    weather_description = json_response['weather'][0]['description'].capitalize()

    air_temperature = round(air_temperature_kelvin - 273, 2)
    feels_like_temperature = round(feels_like_temperature_kelvin - 273, 2)

    weather_dictionary = {'location': location_name +
                          ' Weather:', 'description': weather_description,
                          'temperature': str(air_temperature),
                          'feelslike': ', Feels like: ' +
                          str(feels_like_temperature) + ' degrees celcius. '}

    return weather_dictionary
