''' This function is to test the program functions of the smart alarm

    Each function is tested with a single test case and the result is
    printed to the user in the stdout'''

from weather_api import get_weather


def test_weather():
    ''' test get weather function of the module '''

    weather_return = get_weather()
    assert type(weather_return) is dict, 'Weather Return Function: FAILED'
