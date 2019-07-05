"""
A server to transfer notifications across various interfaces

:http_server_address str
    The address to host the http server

:socket_server_address str
    The address to host the socket server
"""
import os
import signal
from functools import partial
from os.path import join, dirname
from random import randint
from subprocess import Popen, CalledProcessError
from threading import Event

import sys
from time import sleep

import atexit
from prettyparse import create_parser

from notify_server.events import EventSystem
from notify_server.socket_server import SocketServer


def popen_check(command, boot_time=0.2, **kwargs):
    proc = Popen(command, **kwargs)
    sleep(boot_time)
    ret = proc.poll()
    if ret is not None:
        raise CalledProcessError(ret, ' '.join(command))
    return proc


def main():
    parser = create_parser(__doc__)
    args = parser.parse_args()
    try:
        socket_host, socket_port = args.socket_server_address.split(':')
        socket_port = int(socket_port)
    except ValueError:
        parser.error('Invalid socket server address')
        raise SystemExit(1)

    gunicorn = join(dirname(sys.executable), 'gunicorn')

    ruko_host = 'localhost'
    ruko_port = randint(49152, 65535)

    ruko_server = popen_check([
        'ruko-server', '--in-memory', '{}:{}'.format(ruko_host, ruko_port)
    ])
    atexit.register(partial(ruko_server.send_signal, signal.SIGINT))

    flask_server = popen_check([gunicorn, 'notify_server.flask_server:app', '-w', '4', '-b', args.http_server_address], env=dict(
        os.environ, NS_RUKO_HOST=ruko_host, NS_RUKO_PORT=str(ruko_port)
    ))
    atexit.register(partial(flask_server.send_signal, signal.SIGINT))

    event_system = EventSystem(ruko_host, ruko_port)
    socket_server = SocketServer(socket_host, socket_port, event_system)
    socket_server.start()
    atexit.register(socket_server.stop)

    try:
        Event().wait()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
