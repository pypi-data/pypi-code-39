import asyncio
import atexit
import requests
import time

DEFAULT_DOMAIN = "wac-robot-hub.herokuapp.com"

class Robot:
    def __init__(
        self,
        name=None,
        domain=DEFAULT_DOMAIN,
        left_mod=1.0,
        right_mod=1.0,
        verbose=False,
    ):
        self.name = name
        self.domain = domain
        self.left_mod = left_mod
        self.right_mod = right_mod
        self.verbose = verbose
        self.commands = []

        atexit.register(self._done)

    # Wheels have been temporarily reversed until the board code is updated.
    # Left = right, Right = left, etc etc.
    def wheels(self, left, right):
        l = -1 * round(left * self.left_mod)
        r = -1 * round(right * self.right_mod)
        self._queue("w=%d,%d" % (r, l))

    def stop(self):
        self.wheels(0, 0)

    def led(self, r, g, b):
        self._queue("l=%d,%d,%d" % (r, g, b))

    def buzzer(self, hertz=1000, pulse=1023):
        self._queue("b=%d,%d" % (hertz, pulse))

    def buzzer_off(self):
        self._queue("b=off")

    def sleep(self, t):
        self._queue("s=%d" % (t * 1000))

    def _get_headers(self):
        return {}

    def _get_url(self):
        return "https://%s/command/%s" % (self.domain, self.name)

    def _queue(self, message):
        self.commands.append(message)

    def _done(self):
        self.stop()
        self.led(0, 0, 0)
        self.buzzer_off()
        self._send()

    def _send(self):
        body = bytearray("\r\n".join(self.commands), 'utf-8')

        if len(body) > 2000:
            return print("Too many instructions.")

        if self.verbose:
            print(body)

        resp = requests.post(self._get_url(), headers=self._get_headers(), data=body)

        if resp.status_code >= 400:
            print("Unable to deliver instructions")
