import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

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
            'filename': fr'{BASE_DIR}\src\log.log',
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
