import asyncio
import atexit
import requests
import time
from websocket import create_connection

ENDPOINT = "/command"

class Robot:
  def __init__(self, name, left_mod=1.0, right_mod=1.0, enable_sockets=True):
    self.name = name
    self.enable_sockets = enable_sockets
    self.ws = create_connection("ws://%s.local%s" % (name, ENDPOINT))
    self.url = "http://%s.local%s" % (name, ENDPOINT)
    self.left_mod = left_mod
    self.right_mod = right_mod

    atexit.register(self._done)

  def wheels(self, left, right):
    l = round(left * self.left_mod)
    r = round(right * self.right_mod)
    print("Left: %d, Right: %d" % (l, r))
    self._send("left=%d&right=%d" % (l, r))

  def stop(self):
    self.wheels(0, 0)

  def led_on(self):
    print("LED: on")
    self._send("led=on")

  def led_off(self):
    print("LED: off")
    self._send("led=off")

  def led_rgb(self, r, g, b):
    print("LED: %d,%d,%d" % (r, g, b))
    self._send("led=%d,%d,%d" % (r, g, b))

  def buzzer_on(self):
    print("Buzzer: on")
    self._send("buzzer=on")

  def buzzer_off(self):
    print("Buzzer: off")
    self._send("buzzer=off")

  def pause(self):
    print("Pause")
    self._send("pause=true")

  def resume(self):
    print("Resume")
    self._send("resume=true")

  def _done(self):
    self.stop()
    self.led_off()
    self.buzzer_off()

  def _send(self, message):
    if self.enable_sockets:
      self.ws.send(message)
    else:
      requests.get("%s?%s" % (self.url, message))

