from multiprocessing import Process
from multiprocessing import Pipe
import traceback

from functools import wraps


def restricted(func):
  @wraps(func)
  def wrapped(self, update, context, *args, **kwargs):
    user_id = update.effective_user.id
    if user_id not in self.allowed_users:
      print("Unauthorized access denied for {}.".format(user_id))
      return None
    try:
      return func(self, update, context, *args, **kwargs)
    except Exception as error:
      self.error_callback(update, context, error)
  return wrapped


class ProcessWithException(Process):
  def __init__(self, *args, callback=None, **kwargs):
    super().__init__(*args, **kwargs)
    self._pconn, self._cconn = Pipe()
    self._exception = None
    self.callback = callback

  def run(self):
    try:
      Process.run(self)
      self._cconn.send(None)
    except Exception as error:
      if self.callback:
        self.callback(error)
      tb = traceback.format_exc()
      error_name = error.__class__.__name__
      self._cconn.send((error_name, error, tb))
      raise error

  @property
  def exception(self):
    if self._pconn.poll():
      self._exception = self._pconn.recv()
    return self._exception


def rip_scrap_process(cookie_name=None, cookie_value=None, save_dir=None, _test_mode=False):

  incapsula_cookie = None
  if cookie_name and cookie_value:
    incapsula_cookie = {}
    incapsula_cookie[cookie_name] = cookie_value

  import os
  os.environ['RIP_COUNTER_DATA_DIR'] = str(save_dir)

  import asyncio

  import rip_counter

  print(incapsula_cookie)

  captcha_solver = rip_counter.CaptchaNetSolver(preload_model=True)

  scraper = rip_counter.RIPScraper(captcha_solver=captcha_solver,
                                   incapsula_cookie=incapsula_cookie,
                                   max_captcha_try=20,
                                   shuffle_urls=True,
                                   save_dir=save_dir)

  scrap_task = scraper.scrap(batch_size=64, show_progress=True, _test_mode=_test_mode)

  asyncio.run(scrap_task)

  # Preprocess data
  scraper.process_data()
