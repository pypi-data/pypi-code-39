'''
Created on Monday 27/05/2019

@author: yaztown
'''
from .base_exceptions import ThreadExitException
import signal

from loopie.logging import get_logger
logger = get_logger()


def shutdown_routine(signum, frame):
    sig = signal._int_to_enum(signum,signal.Signals)
    logger.debug('\n\nReceived {}.\n'.format(sig.name))
    raise ThreadExitException()

def register_exit_signal_handler():
    signal.signal(signal.SIGTERM, shutdown_routine)
    signal.signal(signal.SIGINT, shutdown_routine)

'''
    If you are using eclipse or any other IDE to debug your app, then you
    can use the below command to search and kill your. Just change <appname>
    to your app's name.
        
        kill -SIGINT $(ps aux | grep <appname> | grep -v grep| awk '{print $2}')

'''
