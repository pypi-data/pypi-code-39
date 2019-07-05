import asyncio
import atexit
import requests
import time
from websocket import create_connection

ENDPOINT = "/command"


class Robot:
    def __init__(
        self,
        name,
        left_mod=1.0,
        right_mod=1.0,
        enable_sockets=True,
        verbose=False,
    ):
        self.verbose = verbose
        self.name = name
        self.enable_sockets = enable_sockets
        self.ws = create_connection(
            "ws://%s.local%s" % (name, ENDPOINT)
        )
        self.url = "http://%s.local%s" % (name, ENDPOINT)
        self.left_mod = left_mod
        self.right_mod = right_mod

        atexit.register(self._done)

    def wheels(self, left, right):
        l = round(left * self.left_mod)
        r = round(right * self.right_mod)

        if self.verbose:
            print("Left: %d, Right: %d" % (l, r))

        self._send("left=%d&right=%d" % (l, r))

    def stop(self):
        self.wheels(0, 0)

    def led(self, r, g, b):
        if self.verbose:
            print("LED: %d,%d,%d" % (r, g, b))

        self._send("led=%d,%d,%d" % (r, g, b))

    def buzzer(self, hertz, pulse=1023):
        if self.verbose:
            print("Buzzer: %d Hz, %d" % (hertz, pulse))

        self._send("buzzer=%d,%d" % (hertz, pulse))

    def buzzer_off(self):
        if self.verbose:
            print("Buzzer: off")

        self._send("buzzer=off")

    def pause(self):
        if self.verbose:
            print("Pause")

        self._send("pause=true")

    def resume(self):
        if self.verbose:
            print("Resume")

        self._send("resume=true")

    def _done(self):
        self.stop()
        self.led(0, 0, 0)
        self.buzzer_off()

    def _send(self, message):
        if self.enable_sockets:
            self.ws.send(message)
        else:
            requests.get("%s?%s" % (self.url, message))
