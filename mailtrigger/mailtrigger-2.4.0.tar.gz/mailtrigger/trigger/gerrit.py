# -*- coding: utf-8 -*-

import os

from .trigger import Trigger, TriggerException

HELP = ('@gerrit help',
        '@gerrit list',
        '@gerrit restart <host>',
        '@gerrit start <host>',
        '@gerrit stop <host>',
        '@gerrit verify <host>',
        '@gerrit review <host>:<port>',
        '  [--project <PROJECT> | -p <PROJECT>]',
        '  [--branch <BRANCH> | -b <BRANCH>]',
        '  [--message <MESSAGE> | -m <MESSAGE>]',
        '  [--notify <NOTIFYHANDLING> | -n <NOTIFYHANDLING>]',
        '  [--submit | -s]',
        '  [--abandon | --restore]',
        '  [--rebase]',
        '  [--move <BRANCH>]',
        '  [--publish]',
        '  [--json | -j]',
        '  [--delete]',
        '  [--verified <N>] [--code-review <N>]',
        '  [--label Label-Name=<N>]',
        '  [--tag TAG]',
        '  {COMMIT | CHANGEID,PATCHSET}')


class Gerrit(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid gerrit configuration')
        self._debug = config.get('debug', False)
        self._filter = config.get('filter', [])
        self._server = config.get('server', [])

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
        return os.linesep.join(HELP)

    def run(self, event):
        if self._check(event) is False:
            return '', False
        return '', False
