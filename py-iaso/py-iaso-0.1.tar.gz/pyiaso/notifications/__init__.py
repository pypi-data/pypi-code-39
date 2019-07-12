from ..utils import raise_invalid_key, raise_missing_key, print_log
from .helpers.sendgrid import email_sendgrid
from .helpers.console import console_log

class Notification:
    def __init__(self, data_dict):
        self.args = data_dict.get('data', {})
        
        if data_dict.get('enabled', True) == False:
            self.func = lambda *args, **kwargs: True
            return

        if set(data_dict.keys()).isdisjoint(set(['type', 'data'])):
            raise_invalid_key('notifications')

        if data_dict['type'] == 'email_sendgrid':
            self.func = email_sendgrid
        elif data_dict['type'] == 'console':
            self.func = console_log
        else:
            raise_invalid_key('notification: ' + data_dict['type'])


    def __call__(self, check, success):
        self.func(check, success, **self.args)