# -*- coding: utf-8 -*-

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
    PREFIX + 'abandon <host> <commit|changenumber,patchset>',
    PREFIX + 'restore <host> <commit|changenumber,patchset>',
    PREFIX + 'review <host> <commit|changenumber,patchset>',
    PREFIX + 'submit <host> <commit|changenumber,patchset>',
    PREFIX + 'version <host>'
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
            return 'Incorrect host %s' % host
        self._client.connect(hostname=server['host'], port=29418, username=server['user'], password=server['pass'])
        _, stdout, stderr = self._client.exec_command(cmd)
        out, err = stdout.read(), stderr.read()
        self._client.close()
        return out.decode() if len(err.decode()) == 0 else err.decode()

    def _help(self, _):
        _ = self
        return os.linesep.join(HELP)

    def _list(self, _):
        hosts = [item['host'] for item in self._server]
        return os.linesep.join(hosts)

    def _restart(self, msg):
        return 'Unsupported'

    def _start(self, msg):
        return 'Unsupported'

    def _stop(self, msg):
        return 'Unsupported'

    def _abandon(self, msg):
        host, change = msg.split()
        return self._exec('gerrit review --abandon %s' % change, host)

    def _restore(self, msg):
        host, change = msg.split()
        return self._exec('gerrit review --restore %s' % change, host)

    def _review(self, msg):
        host, change = msg.split()
        return self._exec('gerrit review --code-review +2 --verified +1 %s' % change, host)

    def _submit(self, msg):
        host, change = msg.split()
        return self._exec('gerrit review --submit %s' % change, host)

    def _version(self, msg):
        host = msg
        return self._exec('gerrit version', host)

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
        status = False
        for item in lines:
            item = item.strip()
            if len(item) == 0:
                continue
            buf = item.split()
            if buf[0] != PREFIX.strip() or len(buf) < 2:
                continue
            msg.append(self._dispatcher.run(' '.join(buf[1:])))
        if len(msg) != 0:
            status = True
        return os.linesep.join(msg), status

    @staticmethod
    def help():
        return os.linesep.join(HELP)

    def run(self, event):
        if self._check(event) is False:
            return '', False
        return self._dispatch(event['content'])
