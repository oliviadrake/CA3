''' collection of functions that convert times to different formats '''

import time


def current_time() -> str:
    ''' Returns the current time in HHMM format '''
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)


def minutes_to_seconds(minutes: int) -> int:
    '''Converts minutes to seconds'''
    return int(minutes)*60


def hours_to_minutes(hours: int) -> int:
    '''Converts hours to minutes'''
    return int(hours)*60


def hhmm_to_seconds(hhmm: str) -> int:
    '''Converts time in the HHMM format into seconds'''
    if len(hhmm.split(':')) != 2:
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])


def days_to_seconds(days_from_now: int) -> int:
    ''' Converts days into seconds '''
    return days_from_now * 24 * 60 * 60
