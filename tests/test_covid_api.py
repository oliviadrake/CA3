''' This function is to test the program functions of the smart alarm

    Each function is tested with a single test case and the result is
    printed to the user in the stdout'''

from covid_api import get_england_covid_data, get_local_covid_data


def test_england():
    ''' test get england covid function of the module '''

    england_covid_return = get_england_covid_data()
    assert type(england_covid_return) is dict, 'England Covid Function: FAILED'


def test_local():
    ''' test get local covid function of the module '''

    local_covid_return = get_local_covid_data()
    assert type(local_covid_return) is dict, 'Exeter Covid Function: FAILED'
