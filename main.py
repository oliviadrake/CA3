
''' Full functionality for an alarm clock.

    Add alarms and delete them, have notifications pushed
    and be able to delete them, and have alarms read aloud
    when the time is scheduled.

    '''

from datetime import date
import datetime
import time
import sched
import logging
from flask import Flask, render_template, request, Markup
import pyttsx3
from time_conversions import days_to_seconds, hhmm_to_seconds, current_time
import config_file
import time_conversions
import weather_api
import news_api
import covid_api

logging.basicConfig(filename='sys.log', level=logging.DEBUG)
app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
engine = pyttsx3.init()

HTML_FILE = config_file.return_html_filename()

# set blank lists to be populated with values
notifications = []
alarms = []
scheduler = {}


@app.route('/')
def runhtml() -> None:
    ''' Render the HTML template

        Show daily briefing upon opening the alarm clock
        Load any alarms from the log file if the date and time are still
        in the the future and put them into the scheduler and alarms list '''

    # create a list of the contents from the current log file
    # log file will continue to change otherwise, so a snapshot of the
    # already open log will be correct and not create an infinite loop

    log = []
    list_of_alarms = []
    log_file = open('sys.log', 'r')
    for each_line in log_file:
        log.append(each_line)
    log_file.close()

    # create a list of alarms found in log file
    for line in log:
        if "INFO:root:{'date':" in line:
            list_of_alarms.append(line[10:])

    list_of_alarms = list(dict.fromkeys(list_of_alarms))

    # for every alarm, extract information from the dictionary
    for each_dictio in list_of_alarms:
        dictionary = eval(each_dictio)

        alarm_date = dictionary['date']
        alarm_hhmm = dictionary['time']
        label = dictionary['label']
        weather = dictionary['weather']
        news = dictionary['news']

        delay = hhmm_to_seconds(
            alarm_hhmm) - hhmm_to_seconds(current_time())
        alarm_date_in_date = (datetime.datetime.strptime(alarm_date, '%Y-%m-%d')).date()

        # check the alarms havent already gone off, if not add to sched
        if alarm_date == str(date.today()) or alarm_date_in_date > date.today():
            if delay > 0:
                add_alarm(alarm_hhmm, alarm_date, label, news, weather)

    logging.info("Any previous alarms rendered")

    # show newly updated info in a daily briefing
    show_daily_briefing()

    # schedule daily briefing every day for a year
    twenty_four_hours = (24*60)
    for each_day in range(0, 365):
        s.enter(twenty_four_hours, 1, show_daily_briefing)
        twenty_four_hours = twenty_four_hours * (each_day + 1)

    logging.info("Daily Briefing Shown")

    return render_template(HTML_FILE, alarms=alarms,
                           title='COVID Smart Alarm Clock',
                           notifications=notifications, image='clocks.jpg')


@app.route('/index')
def add_to_scheduler() -> None:
    ''' Once an alarm has been added, inject to HTML frame and scheduler

        Push any notifications that have been requested by the
        user into the scheduler and delete any notificatons or alarms
        the user has requested to delete'''

    s.run(blocking=False)

    # Gather arguments from the URL
    try:  # get alarm time
        alarm_time = request.args.get("alarm")
    except:
        alarm_time = None
        logging.info('No Alarm Time able to extract from URL')
    try:  # get the label of the alarm
        label = request.args.get("two")
    except:
        label = 'Alarm'
        logging.info('No Alarm Label able to extract from URL')
    try:  # get whether the user wants the news briefing or not
        news = request.args.get("news")
    except:
        news = None
        logging.info('News not able to extract from URL because box wasnt checked')
    try:  # get whether the user wants the weather briefing or not
        weather = request.args.get("weather")
    except:
        weather = None
        logging.info('Weather not able to extract from URL because box wasnt checked')
    try:  # check for parameters that show a notification has been deleted
        delete = request.args.get("notif")
    except:
        delete = None
        logging.info('No notifcations to be deleted because user hasnt deleted any')
    try:  # check for parameters that show an alarm has been deleted
        delete_alarm = request.args.get("alarm_item")
    except:
        delete_alarm = ' '
        logging.info('No alarms to be deleted because user hasnt deleted any')

    # When alarm gets added, add to scheduler and add news/ weather
    if alarm_time:
        alarm_hhmm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
        alarm_date = alarm_time[:10]
        add_alarm(alarm_hhmm, alarm_date, label, news, weather)

    # when a notification gets cleared
    if delete:
        for each_notification in notifications:
            if each_notification['title'] == delete:
                notifications.remove(each_notification)
        logging.info("Notification deleted")

    # when an alarm gets cleared
    if delete_alarm:
        for each_alarm in alarms:
            if delete_alarm == each_alarm['title']:
                # clear from list and scheduler
                alarms.remove(each_alarm)
                s.cancel(scheduler[delete_alarm])
                try:
                    s.cancel(scheduler[delete_alarm + '1'])
                except:
                    pass
                try:
                    s.cancel(scheduler[delete_alarm + '2'])
                except:
                    pass
        logging.info("Alarm Deleted")

    return render_template(HTML_FILE, alarms=alarms,
                           title='COVID Smart Alarm Clock',
                           notifications=notifications, image='clocks.jpg')


def read_aloud(alarm: str, time_value: str) -> None:
    ''' Read aloud alarm using PyTTSx3

        use alarm label as the alarm sound'''

    # gather info from apis
    weather_dictionary = weather_api.get_weather()
    local = covid_api.get_local_covid_data()
    temperature = float(weather_dictionary['temperature'])

    # create an alarm message
    if temperature < 10:
        cute_message = 'Make sure you wear a coat!!!'
    elif temperature > 25:
        cute_message = "Don't forget your sun cream!!!"
    else:
        cute_message = 'Today is a beautiful day!!!'

    speech = alarm + '.  ' + cute_message + '  the local temperature is ' + \
        str(temperature) + ' degrees celcius.' + ' The COVID 19 infection rate in your local area is ' + \
        str(int(local["newCasesByPublishDate"]) / 100000) + ' per 100000 people'

    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop Error')
    engine.say(speech)
    engine.runAndWait()
    logging.info("Alarm Read Aloud")

    # remove alarm from list of alarms because its done
    for each_value in alarms:
        if time_value + ' Today' == each_value['title']:
            alarms.remove(each_value)
            logging.info("Alarm Removed from frame")


def show_news() -> None:
    ''' Use news api to add top stories into the notification list

    append notifications list with a dictionary where the title value is
    taken from the news api's title for each article and the content values
    are from the rest of the info'''

    news_dictionary = news_api.get_top_stories()

    # for every headline, extract information from dictionary
    for each_headline in news_dictionary:
        title = each_headline['title']

        # make URL a clickable link
        markupstring = "<a href='%s'>%s</a>" % (each_headline['url'], 'See Article Here')
        contents = each_headline['description'] + ' ' + Markup(markupstring)

        notifications.insert(0, {'title': title, 'content': contents})
    logging.info('News Shown')


def show_weather() -> None:
    ''' Use weather api to show weather in the notifications list

    append notifications list with a dictionary where the title value is
    taken from the weather api's place name and the content values are from
    the rest of the info '''

    weather_dictionary = weather_api.get_weather()

    temperature = float(weather_dictionary['temperature'])

    if temperature < 10:
        cute_message = 'Make sure you wear a coat!!!'
    elif temperature > 25:
        cute_message = "Don't forget your sun cream!!!"
    else:
        cute_message = 'Today is a beautiful day!!!'

    title = weather_dictionary['location']

    contents = weather_dictionary['description'] + ', Air Temperature is: ' + \
        weather_dictionary['temperature'] + ' degrees celcius' + \
        weather_dictionary['feelslike'] + cute_message

    notifications.insert(0, {'title': title, 'content': contents})
    logging.info("Weather Shown")


def show_daily_briefing() -> None:
    ''' Use all 3 apis to show a daily briefing

        must include: weather, news stories, and covid rates '''

    show_news()
    show_weather()
    local_location = config_file.return_local_location()

    england = covid_api.get_england_covid_data()
    local = covid_api.get_local_covid_data()

    content = ' - New Cases: ' + str(england["newCasesByPublishDate"]) + \
        ' - Total Cumulative Cases: ' + str(england["cumCasesByPublishDate"]) + \
        ' - New Deaths: ' + str(england["newDeathsByPublishDate"]) + \
        ' - Total Cumulative Deaths: ' + str(england["cumDeathsByPublishDate"]) + \
        ' - Infection Rate (per 100,000): ' + \
        str(int(england["newCasesByPublishDate"]) / 100000)

    notifications.insert(
        0, {'title': 'England Covid Report:', 'content': content})

    content = ' - New Cases: ' + str(local["newCasesByPublishDate"]) + \
        ' - Total Cumulative Cases: ' + str(local["cumCasesByPublishDate"]) + \
        ' - New Deaths: ' + str(local["newDeathsByPublishDate"]) + \
        ' - Total Cumulative Deaths: ' + str(local["cumDeathsByPublishDate"]) + \
        ' - Infection Rate (per 100,000): ' + \
        str(int(local["newCasesByPublishDate"]) / 100000)

    notifications.insert(0, {'title': local_location+' Covid Report:', 'content': content})

    notifications.insert(0,
                         {'title': 'Good Morning! Your Daily Briefing:',
                             'content': 'COVID data from yesterday, ' +
                             'top news stories and the weather in your area'})


def add_alarm(alarm_hhmm: str, alarm_date: str, label: str, news: str = None, weather: str = None) -> None:
    ''' Once an alarm has been added, inject to HTML frame and scheduler

        Push any notifications that have been requested by the
        user into the scheduler and delete any notificatons or alarms
        the user has requested to delete'''

    # add all info about the alarm to the logger
    logging.info({'date': alarm_date, 'time': alarm_hhmm,
                  'label': label, 'news': news, 'weather': weather})

    todays_date = str(date.today())
    timesec = time.localtime()
    time_in_seconds = int(time.strftime("%S", timesec))

    if todays_date == alarm_date:
        day = 'Today'
        alarm_title = alarm_hhmm + ' ' + day
        # calculate delay for the alarm
        try:
            delay = hhmm_to_seconds(
                alarm_hhmm) - hhmm_to_seconds(current_time()) - time_in_seconds
        except:
            delay = -1
            label = 'Error'
            logging.error('Time Conversions hhmm to seconds was unsucessful')
    else:
        day = alarm_date
        alarm_date_in_date = datetime.datetime.strptime(alarm_date, '%Y-%m-%d')
        days_between = (alarm_date_in_date.date()) - date.today()
        alarm_title = alarm_hhmm + ' ' + day

        # calculate delay for the alarm
        try:
            delay = days_to_seconds(int(days_between.days)) + (hhmm_to_seconds(
                alarm_hhmm) - hhmm_to_seconds(current_time()) - time_in_seconds)

        except:
            delay = -1
            label = 'Error'
            logging.error('Time Conversions were unsucessful')

    if delay > 0:
        # add alarm to alarms list
        alarms.insert(0, {'title': alarm_title, 'content': label})

        # add the alarm to scheduler
        scheduler[alarm_title] = s.enter(delay, 1, read_aloud, kwargs={
                                         'alarm': label, 'time_value': alarm_hhmm})
        logging.info("Alarm Scheduled")

        if news:
            scheduler[alarm_title+'1'] = s.enter(delay, 1, show_news)
            logging.info('News show added to scheduler')
        if weather:
            scheduler[alarm_title+'2'] = s.enter(delay, 1, show_weather)
            logging.info('Weather show added to scheduler')
    else:
        logging.error('Negative Delay Entered')


def tests() -> None:
    ''' Selection of unit tests on all functions with an expected outcome

    to be run before the startup of the project to notify user of any errors
    before program begins

    LIST OF OTHER FUNCTIONS IN PROJECT, HOWEVER NONE RETURN ANYTHING:
    # show_daily_briefing()
    # show_weather()
    # show_news()
    # read_aloud()
    # add_to_scheduler()
    # runhtml() '''

    weather_return = weather_api.get_weather()
    news_return = news_api.get_top_stories()
    england_covid_return = covid_api.get_england_covid_data()
    local_covid_return = covid_api.get_local_covid_data()

    assert isinstance(weather_return, dict), 'Weather Return Function: FAILED'
    assert isinstance(news_return, list), 'News Return Function: FAILED'
    assert isinstance(england_covid_return, dict), 'England Covid Function: FAILED'
    assert isinstance(local_covid_return, dict), 'Local Covid Function: FAILED'

    assert time_conversions.minutes_to_seconds(5) == 300, 'Minutes to Seconds Function test: FAILED'
    assert time_conversions.hours_to_minutes(2) == 120, 'Hours to Minutes Function test: FAILED'
    assert time_conversions.hhmm_to_seconds(
        '11:11') == 40260, 'HHMM to Seconds Function test: FAILED'
    assert time_conversions.days_to_seconds(3) == 259200, 'Days to Seconds test: FAILED'


if __name__ == '__main__':
    try:
        tests()
    except AssertionError as message:
        print(message)
    app.run()
