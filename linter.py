import pylint.lint
pylint_opts = ['main.py', 'news_api.py', 'weather_api.py',
               'covid_api.py', 'time_conversions.py', 'config_file.py']
pylint.lint.Run(pylint_opts)
