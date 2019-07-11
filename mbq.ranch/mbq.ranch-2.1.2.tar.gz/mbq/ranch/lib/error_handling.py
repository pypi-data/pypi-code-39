import logging

from django.db.utils import Error

import rollbar
from celery.app import control

from .. import _collector


logger = logging.getLogger(__name__)


def log_errors_and_send_to_rollbar(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Error:
            # If we receive any database-related exceptions, send SIGTERM--this may not be
            # necessary in every case, but it is safer
            logger.exception("Database error")
            rollbar.report_exc_info()
            control.shutdown()
        except Exception:
            logger.exception("Ranch signal error")
            rollbar.report_exc_info()
            _collector.increment("signal_error", value=1)
            raise

    return wrapper
