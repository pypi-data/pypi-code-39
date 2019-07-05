"""Utilities
"""
import os
import time
import datetime
from decimal import Decimal
from dateutil.tz import gettz


def now_ts():
    """
    ts in ms
    """
    return Decimal(time.time() * 1000)


def now_day():
    """Returns a string with the day of the week in the format:
    Mon, Tue, Wed, Thu, Fri, Sat, Sun
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).strftime('%a')


def hour():
    """
    Returns the current hour
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).hour


def minute():
    """
    Returns the current minute
    """
    return datetime.datetime.now(gettz(os.environ['TZ'])).minute


def tot_min():
    """
    Minutes from 00:00
    """
    return hour() * 60 + minute()


def midday_ts():
    """
    The 12:00 local time ts in ms"""
    today = datetime.datetime.now(gettz(os.environ['TZ']))
    return Decimal(datetime.datetime(today.year, today.month, today.day, 12,
                                     tzinfo=gettz(os.environ['TZ'])).timestamp() * 1e3)


def benchmark(display_func):
    """
    Used to time functions
    :param display_func: function to display the results, e.g. print
    :return:
    """
    def time_it(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            display_func('{name} executed in {time}s'.format(name=func.__name__,
                                                             time=time.perf_counter() - start))
            return res
        return wrapper
    return time_it
