import asyncio
import atexit
import requests
import time
from websocket import create_connection

ENDPOINT = "/stack"


class Robot:
    def __init__(
        self,
        name,
        left_mod=1.0,
        right_mod=1.0,
        enable_sockets=False,
        verbose=False,
    ):
        self.verbose = verbose
        self.name = name
        self.enable_sockets = enable_sockets
        self.left_mod = left_mod
        self.right_mod = right_mod
        self.commands = []

        if enable_sockets:
            self.ws = create_connection(
                "ws://%s.local%s" % (name, ENDPOINT)
            )
        else:
            self.url = "http://%s.local%s" % (name, ENDPOINT)

        atexit.register(self._done)

    def wheels(self, left, right):
        l = round(left * self.left_mod)
        r = round(right * self.right_mod)

        if self.verbose:
            print("Left: %d, Right: %d" % (l, r))

        self._queue("w=%d,%d" % (l, r))

    def stop(self):
        self.wheels(0, 0)

    def led(self, r, g, b):
        if self.verbose:
            print("LED: %d,%d,%d" % (r, g, b))

        self._queue("l=%d,%d,%d" % (r, g, b))

    def buzzer(self, hertz=1000, pulse=1023):
        if self.verbose:
            print("Buzzer: %d Hz, %d" % (hertz, pulse))

        self._queue("b=%d,%d" % (hertz, pulse))

    def buzzer_off(self):
        if self.verbose:
            print("Buzzer: off")

        self._queue("b=off")

    def sleep(self, t):
        if self.verbose:
            print("Sleep: %dms" % (t * 1000))

        self._queue("s=%d" % (t * 1000))

    def _queue(self, message):
        self.commands.append(message)

    def _done(self):
        self.stop()
        self.led(0, 0, 0)
        self.buzzer_off()
        self._send()

    def _send(self):
        body = bytearray("\r\n".join(self.commands), 'utf-8')

        if self.enable_sockets:
            self.ws.send(body)
        else:
            requests.post(self.url, data=body)
