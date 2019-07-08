import logging
import os
import traceback
from pathlib import Path
import datetime

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

from rip_counter.bot.utils import restricted
from rip_counter.bot.utils import ProcessWithException
from rip_counter.bot.utils import rip_scrap_process


class RIPTelegramBot:

  def __init__(self, bot_token=None, allowed_users=None):

    logging.getLogger().setLevel(logging.INFO)
    self.log = logging.getLogger('RIPTelegramBot')
    self.log.setLevel(logging.INFO)

    if not bot_token:
      if not 'RIP_COUNTER_BOT_TOKEN' in os.environ.keys():
        mess = "Env variable 'RIP_COUNTER_BOT_TOKEN' is not set. Please set it."
        raise ValueError(mess)
      self.token = os.environ['RIP_COUNTER_BOT_TOKEN']
    else:
      self.token = bot_token

    if not allowed_users:
      if not 'RIP_COUNTER_BOT_ALLOWED_USERS' in os.environ.keys():
        mess = "Env variable 'RIP_COUNTER_BOT_ALLOWED_USERS' is not set. Please set it."
        raise ValueError(mess)
      self.allowed_users = [int(user_id) for user_id in os.environ['RIP_COUNTER_BOT_ALLOWED_USERS'].split(',')]
    else:
      self.allowed_users = allowed_users

    self.updater = Updater(token=self.token, use_context=True)
    self.dispatcher = self.updater.dispatcher
    self.dispatcher.add_error_handler(self.error_callback)

    # Add handlers
    self.dispatcher.add_handler(CommandHandler('hello', self.hello))
    self.dispatcher.add_handler(CommandHandler('status', self.status))
    self.dispatcher.add_handler(CommandHandler('start', self.start))
    self.dispatcher.add_handler(CommandHandler('stop', self.stop))
    self.dispatcher.add_handler(CommandHandler('log', self.log_process))
    self.dispatcher.add_handler(CommandHandler('set_cookie', self.set_cookie))

    # RIP Counter process
    self.process_args = {}
    self.process_args['cookie_name'] = "incap_ses_303_2043128"
    self.process_args['cookie_value'] = "M+otKL5POk133ss9Jnk0BExMH10AAAAAyM8+JLZw1q3nfwIZMFZehA=="
    self.process_args['_test_mode'] = False
    self.proc = None
    self.start_date = None
    self.log_path = None

    if not 'RIP_COUNTER_DATA_DIR' in os.environ.keys():
      mess = "Env variable 'RIP_COUNTER_DATA_DIR' is not set. Please set it."
      raise ValueError(mess)
    self.process_args['save_dir'] = os.environ['RIP_COUNTER_DATA_DIR']

  def __call__(self, non_blocking=False):
    self.log.info("Starting the bot...")
    self.updater.start_polling(clean=True)
    if not non_blocking:
      self.updater.idle()

  def _send(self, context, update, mess):
    context.bot.send_message(chat_id=update.message.chat_id, text=mess,
                             parse_mode=telegram.ParseMode.MARKDOWN)

  # pylint: disable=unused-argument
  def error_callback(self, update, context, error=None):
    if not error:
      error = context.error
    error_message = traceback.print_tb(error.__traceback__)
    self.log.error(error_message)
    self.log.error(error)

  @restricted
  def hello(self, update, context):
    mess = "What can I do for you?"
    self._send(context, update, mess)

  @restricted
  def status(self, update, context):
    if self.proc and self.proc.is_alive():
      start_time = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
      duration = (datetime.datetime.now() - self.start_date).total_seconds()
      duration = duration // 3600
      mess = f"A process is already running for {duration:.1f}h and started at {start_time}."
      self._send(context, update, mess)
    elif self.proc and self.proc.exception:
      _, error, tb = self.proc.exception
      mess = f"Last run ended with an exception: `{error}`"
      self._send(context, update, mess)
      mess = f"```\n{tb}\n```"
      self._send(context, update, mess)
    else:
      mess = "No process is running."
      self._send(context, update, mess)

  @restricted
  def start(self, update, context):

    if self.proc and self.proc.is_alive():
      start_time = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
      duration = (datetime.datetime.now() - self.start_date).total_seconds()
      duration = duration // 3600
      mess = f"A process is already running for {duration:.1f}h and started at {start_time}."
      self._send(context, update, mess)
    else:
      self.proc = ProcessWithException(target=rip_scrap_process, kwargs=self.process_args)
      self.proc.start()

      self.start_date = datetime.datetime.now()
      self.log_path = Path(self.process_args['save_dir']) / "scraper.log"

      mess = "Process correctly started."
      self._send(context, update, mess)

  @restricted
  def stop(self, update, context):
    if not self.proc or (self.proc and not self.proc.is_alive()):
      mess = "Can't stop since no proces are running."
      self._send(context, update, mess)
    else:
      self.proc.terminate()
      self.proc.kill()
      mess = "Process stopped."
      self._send(context, update, mess)

  @restricted
  def log_process(self, update, context):
    if self.log_path and self.log_path.is_file():
      with open(self.log_path) as f:
        last_lines = f.readlines()[-5:]
      last_lines = "\n".join(last_lines)
      last_lines = f"```{last_lines}```"
      self._send(context, update, last_lines)
    else:
      mess = f"Log file does not exist: {self.log_path}."
      self._send(context, update, mess)

  @restricted
  def set_cookie(self, update, context):
    self.process_args['cookie_name'] = context.args[0]
    self.process_args['cookie_value'] = context.args[1]
    mess = f"Cookie name set to: `{self.process_args['cookie_name']}`."
    self._send(context, update, mess)
    mess = f"Cookie value set to: `{self.process_args['cookie_value']}`."
    self._send(context, update, mess)


def start_bot():
  bot = RIPTelegramBot()
  bot(non_blocking=False)
