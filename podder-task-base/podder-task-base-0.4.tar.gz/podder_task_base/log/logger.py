import datetime
import inspect
import logging
import sys
import time

from .log_setting import LogSetting


class Logger(object):
    def __init__(self):
        self.start_time = time.time()
        self.task_start_time = time.time()
        self.setting = LogSetting().load()
        self.logger = logging.getLogger('podder.task')
        self.logger.propagate = False
        log_format = self.setting["task_log_format"]
        log_level = self.setting["task_log_level"]
        self.logger.setLevel(log_level)
        self._add_default_handler(log_format, log_level)

    def init_tasktime(self):
        self.task_start_time = time.time()

    def fatal(self, msg, *args, **kwargs):
        # fatal -> critical(python logger)
        self.logger.critical(msg, extra=self._create_extra(), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, extra=self._create_extra(), *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        # warn -> warning(python logger)
        self.logger.warning(msg, extra=self._create_extra(), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, extra=self._create_extra(), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, extra=self._create_extra(), *args, **kwargs)

    def trace(self, msg, *args, **kwargs):
        # trace -> notset(python logger)
        self.logger.log(logging.NOTSET, msg, extra=self._create_extra(), *args, **kwargs)

    def log(self, msg, *args, **kwargs):
        self.logger.log(msg, extra=self._create_extra(), *args, **kwargs)

    # private
    def _create_extra(self):
        ex = {'progresstime': str(round((time.time() - self.start_time), 3)),
              'tasktime': str(round((time.time() - self.task_start_time), 3)),
              'taskname': str(self.setting["task_name"])}
        caller_info = sys._getframe(2)  # caller of 2 level depth
        module_info = inspect.getmodule(caller_info)
        script_info = inspect.getsourcelines(caller_info)[1]
        ex['scriptinfo'] = "%s:%s" % (module_info, script_info)
        # original time code, because logging "datefmt" is not support microsecond
        now = datetime.datetime.now()
        ex['time'] = now.strftime("%Y-%m-%d %H:%M:%S.") + "%06d" % now.microsecond
        return ex

    def _add_default_handler(self, log_format, log_level):
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter(fmt=log_format, datefmt='%Y-%m-%d %H:%M:%S'))
        self.logger.addHandler(handler)


def class_logger(cls):
    global _is_logged
    if _is_logged is False:
        logging.basicConfig()
        _is_logged = Logger()

    cls.logger = _is_logged
    return cls


_is_logged = False
