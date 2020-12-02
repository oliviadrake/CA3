''' gets information from the covid module and returns relevant data '''

from uk_covid19 import Cov19API
from config_file import return_local_location


def get_england_covid_data():
    ''' Reads the covid data from Public Health England

        Returns a dictionary of yesterdays statistics '''

    england_only = ['areaType=nation', 'areaName=England']

    cases_and_deaths = {"date": "date", "areaName": "areaName",
                        "newCasesByPublishDate": "newCasesByPublishDate",
                        "cumCasesByPublishDate": "cumCasesByPublishDate",
                        "newDeathsByPublishDate": "newDeaths28DaysByPublishDate",
                        "cumDeathsByPublishDate": "cumDeaths28DaysByPublishDate"}

    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    covid_data = api.get_json()
    covid_data = covid_data["data"]

    return covid_data[0]


def get_local_covid_data():
    '''Reads the covid data from Public Health England

        Returns a dictionary of yesterdays statistics in local location'''
    location = return_local_location()
    local_location = ['areaName='+location]

    cases_and_deaths = {"date": "date", "areaName": "areaName",
                        "newCasesByPublishDate": "newCasesByPublishDate",
                        "cumCasesByPublishDate": "cumCasesByPublishDate",
                        "newDeathsByPublishDate": "newDeaths28DaysByPublishDate",
                        "cumDeathsByPublishDate": "cumDeaths28DaysByPublishDate"}

    api = Cov19API(filters=local_location, structure=cases_and_deaths)
    covid_data = api.get_json()
    covid_data = covid_data["data"]

    return covid_data[0]
