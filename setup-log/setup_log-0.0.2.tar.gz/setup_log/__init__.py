"""helper to setup logging to write log file for simple usage.
eg:
```
from setup_log import setup_log
setup_log('myapp')
```
log to file 'myapp.%F.%H%M%S.log' with format
    '%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(funcName)s %(message)s'
and datefmt
    '%Y-%m-%d.%H:%M:%S'
`setup_log(console_level=99)` to disable console output
`setup_log(file_level=99)` to disable file output
"""
import logging
import logging.config
import time

name = 'setup_log'

def setup_log(file_prefix='log',
              file_strftime='%F.%H%M%S',
              console_level=logging.DEBUG,
              file_level=logging.DEBUG):
    """setup logging, log file will be prefix-file_strftime.log
    to disable console output, set console_level=logging.CRITICAL+1
    """
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s.%(msecs)03d %(levelname)s %(name)s %(funcName)s %(message)s',
                'datefmt': '%Y-%m-%d.%H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'level': console_level,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'file': {
                'level': file_level,
                'class': 'logging.FileHandler',
                'filename': time.strftime('{}-{}.log'.format(file_prefix, file_strftime),
                                          time.localtime()),
                'mode': 'a',
                'formatter': 'default',
            },
        },
        # default logger for logging.getLogger('anything')
        'root': {'handlers': ['console', 'file'], 'level': 'DEBUG', },
        'loggers': {
            # 'app': {'handlers': ['console', 'file'], 'level': 'DEBUG', 'propagate': False,},
            # disable requests debug message
            'requests': {'handlers': ['console', 'file'], 'level': 'WARNING', 'propagate': False},
            # disable requests debug message
            'urllib3': {'handlers': ['console', 'file'], 'level': 'WARNING', 'propagate': False},
            # disable requests debug message
            'requests_oauthlib.oauth2_session': {
                'handlers': ['console', 'file'], 'level': 'WARNING', 'propagate': False
            },
        },
    }
    if console_level > logging.CRITICAL:
        del config['handlers']['console']
        for logger in [config['root']] + list(config['loggers'].values()):
            if 'console' in logger['handlers']:
                logger['handlers'].remove('console')
    if file_level > logging.CRITICAL:
        del config['handlers']['file']
        for logger in [config['root']] + list(config['loggers'].values()):
            if 'file' in logger['handlers']:
                logger['handlers'].remove('file')
    logging.config.dictConfig(config)


if __name__ == '__main__':
    #pylint: disable=invalid-name
    # as test, run `python3 -m setup_log.__init__`
    setup_log('test-logger')
    log = logging.getLogger('app')
    log.info('here is my log')
    log.critical('BAD things happened')
