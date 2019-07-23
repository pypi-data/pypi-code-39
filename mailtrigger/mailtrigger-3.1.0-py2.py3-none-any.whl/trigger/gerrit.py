# -*- coding: utf-8 -*-

import json
import os
import paramiko

from .trigger import Trigger, TriggerException

PREFIX = '@gerrit '

HELP = (
    PREFIX + 'help',
    PREFIX + 'list',
    PREFIX + 'restart <host>',
    PREFIX + 'start <host>',
    PREFIX + 'stop <host>',
    PREFIX + 'version <host>',
    PREFIX + 'abandon <host> <changenumber>',
    PREFIX + 'restore <host> <changenumber>',
    PREFIX + 'review <host> <changenumber>',
    PREFIX + 'submit <host> <changenumber>'
)


class Dispatcher(object):
    def __init__(self, config):
        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._dispatcher = {
            'help': self._help,
            'list': self._list,
            'restart': self._restart,
            'start': self._start,
            'stop': self._stop,
            'abandon': self._abandon,
            'restore': self._restore,
            'review': self._review,
            'submit': self._submit,
            'version': self._version
        }
        self._server = config.get('server', [])

    def _exec(self, cmd, host):
        def _exec_helper(host):
            buf = None
            for item in self._server:
                if host == item['host']:
                    buf = item
                    break
            return buf
        server = _exec_helper(host)
        if server is None:
            return 'Incorrect host %s' % host, False
        self._client.connect(hostname=server['host'], port=29418, username=server['user'], password=server['pass'])
        _, stdout, stderr = self._client.exec_command(cmd)
        out, err = stdout.read(), stderr.read()
        self._client.close()
        msg = out.decode() if len(err.decode()) == 0 else err.decode()
        status = True if len(err.decode()) == 0 else False
        return msg, status

    def _help(self, _):
        _ = self
        return os.linesep.join(HELP), True

    def _list(self, _):
        hosts = [item['host'] for item in self._server]
        return os.linesep.join(hosts), True

    def _restart(self, msg):
        return 'Unsupported', False

    def _start(self, msg):
        return 'Unsupported', False

    def _stop(self, msg):
        return 'Unsupported', False

    def _abandon(self, msg):
        host, change = msg.split()
        result, status = self._query(msg)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --abandon %s,%s' % (change, result['currentPatchSet']['number']), host)
        msg = 'Change %s abandoned' % change if status is True else 'Change %s is not abandoned' % change
        return msg, status

    def _query(self, msg):
        host, change = msg.split()
        msg, status = self._exec('gerrit query --current-patch-set --format=JSON change:%s' % change, host)
        msg = msg[:msg.find('{"type":"stats","rowCount":1')] if status is True else 'Change %s is not queried'
        return msg, status

    def _restore(self, msg):
        host, change = msg.split()
        result, status = self._query(msg)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --restore %s,%s' % (change, result['currentPatchSet']['number']), host)
        msg = 'Change %s restored' % change if status is True else 'Change %s is not restore' % change
        return msg, status

    def _review(self, msg):
        host, change = msg.split()
        result, status = self._query(msg)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --code-review +2 --verified +1 %s,%s'
                                     % (change, result['currentPatchSet']['number']), host)
        msg = 'Change %s reviewed' % change if status is True else 'Change %s is not reviewed' % change
        return msg, status

    def _submit(self, msg):
        host, change = msg.split()
        result, status = self._query(msg)
        if status is True:
            result = json.loads(result)
            msg, status = self._exec('gerrit review --autosubmit +1 --code-review +2 --presubmit-ready +1 --presubmit-verified +1 --verified +1 %s,%s'
                                     % (change, result['currentPatchSet']['number']), host)
            if status is True:
                msg, status = self._exec('gerrit review --submit %s,%s' % (change, result['currentPatchSet']['number']), host)
        msg = 'Change %s submitted' % change if status is True else 'Change %s is not submitted' % change
        return msg, status

    def _version(self, msg):
        host = msg
        msg, status = self._exec('gerrit version', host)
        msg = msg if status is True else 'Version not found'
        return msg, status

    def run(self, msg):
        msg = msg.split()
        buf = ' '.join(msg[1:]) if len(msg) > 1 else ''
        return self._dispatcher[msg[0]](buf)


class Gerrit(Trigger):
    def __init__(self, config):
        if config is None:
            raise TriggerException('invalid gerrit configuration')
        self._debug = config.get('debug', False)
        self._dispatcher = Dispatcher(config)
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

    def _dispatch(self, content):
        lines = content.split('\n')
        msg = []
        for item in lines:
            item = item.strip()
            if len(item) == 0:
                continue
            buf = item.split()
            if buf[0] != PREFIX.strip() or len(buf) < 2:
                continue
            _msg, _ = self._dispatcher.run(' '.join(buf[1:]))
            msg.append(_msg)
        if len(msg) != 0:
            msg = os.linesep.join(msg)
            status = True
        else:
            msg = 'Failed to dispatch content'
            status = False
        return msg, status

    @staticmethod
    def help():
        return os.linesep.join(HELP)

    def run(self, event):
        if self._check(event) is False:
            return 'Failed to check event', False
        return self._dispatch(event['content'])
