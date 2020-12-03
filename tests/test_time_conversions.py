''' This function is to test the program functions of the smart alarm

    Each function is tested with a single test case and the result is
    printed to the user in the stdout'''

from time_conversions import minutes_to_seconds, hours_to_minutes, hhmm_to_seconds, days_to_seconds


def test_minutes_to_seconds():
    ''' test minutes_to_seconds function from module '''

    assert minutes_to_seconds(5) == 300, 'Minutes to Seconds Function test: FAILED'


def test_hours_to_minutes():
    ''' test the hours_to_minutes function of the module '''

    assert hours_to_minutes(2) == 120, 'Hours to Minutes Function test: FAILED'


def test_hhmm_to_seconds():
    ''' test the hhmm_to_seconds function of the module '''

    assert hhmm_to_seconds('11:11') == 40260, 'HHMM to Seconds Function test: FAILED'


def test_days_to_seconds():
    ''' test the days to seconds function of the module '''

    assert days_to_seconds(3) == 259200, 'Days to Seconds test: FAILED'
