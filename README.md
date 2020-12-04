# Project Specification
Since the outbreak of COVID-19 the day-to-day routine for many people has been disrupted and
the instability of our environment means we have to be adaptable to current events. Keeping up-to date with the rapidly
changing local and national infection rates and regularly updated government guidelines has become a daily challenge
for many as well as keeping track of the weather and plans that are often changed at short notice.
Smart systems are automated systems that adapt to input data streams and alarm clocks are an
everyday item that we use to schedule our lives. This project encapsulates the scope for a smart alarm clock that can
access information about the COVID infection rate and provide scheduled updates about the weather
and the news and engage with us through a lightweight interface as a smart covid-aware alarm clock.

# Folder Hierarchy/Structure
- 'CA3' folder
    - main.py
    - weather_api.py
    - news_api.py
    - covid_api.py
    - time_conversions.py
    - config_file.py
    - sys.log
    - linter.py
    - README.txt
    - 'templates' folder
        - index.html (if not using index.html, heres where to put your HTML file)
    - 'tests' folder
        - test_covid_api.py
        - test_time_conversions.py
        - test_news_api.py
        - test_weather_api.py
    - 'static' folder
        - 'images' folder
            - clocks.jpg

# Configuration File
Contained within the config file is everything that could be used to customise the app for redeployment.
Here is where to adjust any variables that are customisable. To run this app you will need an API key for
the Openweathermap API (https://openweathermap.org) and the News API(https://newsapi.org/). Store these
API keys where instructed in the config file. Base URLs for each API are contained within the config file,
ensure these are up to date before running the code.

Also stored in the config file is the filepath for the log file.

The HTML template is accessed in the code through the config file, make sure the name of the HTML file name
is correct in the config file. Also ensure the HTML file is stored in the 'CA3' folder (or CA3-main if downloaded from github) in the 'templates' folder.
(/CA3/templates/'your_html_file'.html)

Your local location should be stored in the config file, update the function with your city name before running.

# Testing
To run each test in the 'tests' folder, use pytest:
From within the CA3 directory (or CA3-main if downloaded from github) run the command 'python -m pytest'

When the main code is run, a testing function will run and show an error to show a function
failed a test before any of the code is run to save hassle for the user.

Pylint: to do a linter test, run the linter.py code from within the CA3 directory

# Running the code
Make sure the most recent version of python is installed.
Firstly ensure all of these external modules have been pip installed: Flask, PyTTSx3, uk-covid19, pytest, pylint, requests.
Ensure config file has been completely customised, all folders are in correct hierarchy as explained above, and you are
within the 'CA3' directory in the terminal (or CA3-main if downloaded from github).
Run the 'main.py' code, in a browser enter '127.0.0.1:5000/' to access alarm clock.
