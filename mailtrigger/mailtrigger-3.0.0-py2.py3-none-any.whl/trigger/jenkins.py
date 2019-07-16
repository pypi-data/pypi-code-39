# -*- coding: utf-8 -*-

from .trigger import Trigger, TriggerException


class Jenkins(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid jenkins configuration')
        self._debug = config.get('debug', False)
        self._filter = config.get('filter', None)

    def _check(self, event):
        def _check_helper(data, event):
            if event is None:
                return False
            sender = data.get('from', None)
            if sender is None or event['from'] != sender:
                return False
            subject = data.get('subject', '').strip()
            if len(subject) == 0 or event['subject'].startswith(subject) is False:
                return False
            return True
        ret = False
        for item in self._filter:
            if _check_helper(item, event) is True:
                ret = True
                break
        return ret

    @staticmethod
    def help():
        return ''

    def run(self, event):
        if self._check(event) is False:
            return '', False
        return '', False
