''' Adaptable File containing all relevant information

    everything that could be used to customise the app for redeployment '''

# file path to log file is '/CA3/sys.log'


def return_local_location() -> str:
    ''' Return a string of the local city.

    To change your local city name change the returned string: '''

    return 'Exeter'


def return_html_filename() -> str:
    ''' Return the filename of the HTML

    if filename of the HTML file is changed, change it here:
    change the name of the returned string to be the filename '''

    return 'index.html'


def return_weather_api_key() -> str:
    ''' Return API Key for the Weather API

        To insert your own API Key, change the return value,
        to a string containing just your API key'''
    return ''


def return_news_api_key() -> str:
    ''' Return API Key for the News API

        To insert your own API Key, change the return value,
        to a string containing just your API key'''
    return ''


def return_weather_url() -> str:
    ''' Return the base URL for the weather API

        If base URL ever changes, replace returned string with new URL '''
    return 'http://api.openweathermap.org/data/2.5/weather?'


def return_news_url() -> str:
    ''' Return the base URL for the news API

        If base URL ever changes, replace returned string with new URL '''
    return 'http://newsapi.org/v2/top-headlines?'
