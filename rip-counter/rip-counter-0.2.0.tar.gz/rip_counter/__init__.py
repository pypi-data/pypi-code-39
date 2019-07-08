# pylint: disable=wrong-import-position

import logging
import os
from pathlib import Path


def setup_logging(log_path=None, silent=False):
  """Set logging.
  """

  # Reset previous loggers
  for h in logging.getLogger().handlers:
    logging.root.removeHandler(h)
  for f in logging.getLogger().filters:
    logging.root.removeFilter(f)

  formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
  root_logger = logging.getLogger()
  root_logger.setLevel(logging.INFO)

  console_handler = logging.StreamHandler()
  console_handler.setFormatter(formatter)
  root_logger.addHandler(console_handler)

  if "RIP_COUNTER_DATA_DIR" in os.environ.keys():
    log_dir = Path(os.environ['RIP_COUNTER_DATA_DIR'])
    if log_dir.is_dir():
      log_path = log_dir / 'scraper.log'

  # Log to a file.
  if log_path:
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    if not silent:
      root_logger.info("RIP_COUNTER_DATA_DIR env variable detected."
                       f"Logs will be forwarded to {log_path}.")

setup_logging()

from ._version import __version__

from . import utils

from .captcha_solver import manual_captcha_solver
from .captcha_solver import CaptchaNetSolver

from .scraper import RIPScraper

from . import bot
