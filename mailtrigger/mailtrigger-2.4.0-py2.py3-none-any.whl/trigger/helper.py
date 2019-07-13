# -*- coding: utf-8 -*-

import os

from .trigger import Trigger, TriggerException
from ..registry import REGISTRY


class Helper(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid helper configuration')
        self._debug = config.get('debug', False)
        self._filter = config.get('filter', None)
        self._trigger = '@help'

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

    def _parse(self, event):
        lines = event['content'].splitlines()
        ret = False
        for item in lines:
            if self._trigger == item.strip():
                ret = True
                break
        return ret

    @staticmethod
    def help():
        return ''

    def run(self, event):
        if self._check(event) is False:
            return '', False
        if self._parse(event) is False:
            return '', False
        msg = []
        for item in REGISTRY:
            msg.append(item['class'].help())
        return os.linesep.join(msg), True
