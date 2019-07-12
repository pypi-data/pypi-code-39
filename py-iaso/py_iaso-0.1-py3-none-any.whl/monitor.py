import os
import yaml
import functools
import time
from importlib import import_module

from .checks import Check
from .actions import Action
from .notifications import Notification
from .utils import raise_invalid_key, raise_missing_key, print_log

class Monitor:
    def __init__(self, config_file=None):
        # Default config file
        if not config_file:
            config_file = 'config.yaml'

        # Parse config file
        try:
            fp = open(os.path.abspath(config_file), "r")
            self.config = yaml.load(fp, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            raise FileNotFoundError('Cannot open config file: ' + str(e)) from e
        except yaml.parser.ParserError as e:
            raise RuntimeError('ParserError: ' + str(e)) from e

        # Set some attributes (int values)
        # They must be > 1 (especially repeat!)
        for k in ('sleep_time', 'repeat', 'repeat_sleep_factor'):
            val = self.get_key(k)
            try:
                val = int(self.get_key(k))
            except ValueError:
                raise_invalid_key(k)
            if val < 1:
                raise_invalid_key(k)
            setattr(self, k, val)
                
        self.checks = [Check(c) for c in self.get_key('checks')]
        if not self.checks:
            raise RuntimeError('No checks defined in config')
        self.actions = [Action(a) for a in self.get_key('actions')]
        if not self.actions:
            raise RuntimeError('No actions defined in config')
        self.notifications = [Notification(n) for n in self.get_key('notifications')]
        if not self.notifications:
            raise RuntimeError('No notifications defined in config')

    def get_key(self, key):
        try:
            return self.config[key]
        except KeyError:
            raise_missing_key(key)

    def run(self):
        while True:
            checks = self.checks
            results = [check() for check in checks]
            
            # Checks are broken?
            if not results or len(set(results)) > 1 or set(results).pop() == False:
                failed_checks = checks
                # Repeat the checks
                for rep in range(0, self.repeat):
                    # Run the actions
                    for action in self.actions:
                        action()

                    print_log('Check #{}'.format(rep+1))
                    
                    # Run the checks again
                    failed_checks = [c for c, r in zip(failed_checks, results) if not r]
                    results = [check() for check in failed_checks]
                    
                    print_log('Extra sleep...')
                    time.sleep(self.sleep_time*self.repeat_sleep_factor)                    

                # Process notifications
                for check, result in zip(failed_checks, results):
                    for notif in self.notifications:
                        notif(check, result)        

            print_log('Sleeping...')
            time.sleep(self.sleep_time)