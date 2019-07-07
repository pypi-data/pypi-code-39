import time
from celery import shared_task

@shared_task
def do_something_slowly(**kwargs):
    sleep_time  = kwargs.get('sleep', 5)
    time.sleep(sleep_time)

@shared_task
def ping(**kwargs):
    return 'pong'

@shared_task
def hello(msg):
    return msg

