# -*- coding: utf-8 -*-
from threading import Event, Thread

def call_repeatedly(intervalSec, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(intervalSec): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set



from time import sleep
from timeit import default_timer as timer

def timeDurationNoRet(logger, sleepTime = 1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                startTime = timer()

                func(*args, **kwargs)

                elapsed = timer() - startTime

                if float(sleepTime) > (elapsed):
                    sleep(float(sleepTime) - float(elapsed))

                return 

            except Exception as inst:
                # log the exception
                err = "There was an exception in {}. msg:{}".format(func.__name__, inst.args)
                logger.error(err)
                return
        return wrapper
    return decorator

def timeDuration(logger, sleepTime = 1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                startTime = timer()

                retValue = func(*args, **kwargs)

                elapsed = timer() - startTime

                if float(sleepTime) > (elapsed):
                    sleep(float(sleepTime) - float(elapsed))

                return retValue

            except Exception as inst:
                # log the exception
                err = "There was an exception in {}. msg:{}".format(func.__name__, inst.args)
                logger.error(err)
                return None
        return wrapper
    return decorator

