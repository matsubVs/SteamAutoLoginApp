import os

BASE_DIR = os.getcwd()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom_formatter': {
            'format': '{levelname} - {asctime} - {module}: {message}',
            'style': '{'
            },
        },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': r'C:\Users\matsubus\PycharmProjects\AutoLoginSteamProj\src\src\log.log',
            'formatter': 'custom_formatter'
            },
        },
    'loggers': {
        'App': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propogate': True
            }
        }
    }
