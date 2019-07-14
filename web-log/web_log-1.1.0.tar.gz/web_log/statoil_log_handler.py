try:
    import httplib
except ModuleNotFoundError:
    import http.client as httplib  # TODO use requests

import json
import logging

from .web_log_functions import fill_standard_event
import web_log


class StatoilLogHandler(logging.Handler):
    def __init__(self, application, user=None, host=None, path=None):
        """
        Initialize the instance with the application name and optionally the user (if not
        provided the user will be retrieved from the operating system).
        If host is provided it should be on the format "host" or "host:port", but not contain any path. Optional path
        can be given with the path argument.
        """
        logging.Handler.__init__(self)
        self.application = application
        self.user = user
        self.host = host
        if host is None:
            self.host = "{}:{}".format(
                web_log.constants.WEBLOG_SERVER, web_log.constants.WEBLOG_PORT
            )
        self.path = path
        if self.path is None:
            self.path = web_log.constants.WEBLOG_PATH

    def emit(self, record):
        """
        Emit a record.

        Send the record to the Web server as json
        """
        try:
            log_dict = {
                "loglevel": record.levelname,
                "pathname": record.pathname,
                "linenr": record.lineno,
                "log_name": record.name,
            }
            log_dict.update(
                fill_standard_event(
                    self.application,
                    record.getMessage(),
                    extra_info=extra_from_record(record),
                    user=self.user,
                )
            )
            self.postLog(log_dict)
        except Exception:
            self.handleError(record)

    def postLog(self, log_dict):
        host = self.host
        h = httplib.HTTPConnection(host, timeout=web_log.constants.WEBLOG_TIMEOUT)
        url = self.path
        data = json.dumps(log_dict)
        h.putrequest("POST", url)
        # support multiple hosts on one IP address...
        # need to strip optional :port from host, if present
        i = host.find(":")
        if i >= 0:
            host = host[:i]
        h.putheader("Host", host)
        h.putheader("Content-type", "application/json")
        h.putheader("Content-length", str(len(data)))
        h.endheaders()
        h.send(data.encode("utf-8"))
        h.getresponse()  # can't do anything with the result


# Copied from https://github.com/marselester/json-log-formatter/blob/master/json_log_formatter/__init__.py (MIT license)

# Used by the function extra_from_record, these are keywords which it will ignore when extracting the dictionary
# with extra information.
BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


def extra_from_record(record):
    """Returns `extra` dict you passed to logger.
    The `extra` keyword argument is used to populate the `__dict__` of
    the `LogRecord`.
    """
    return {
        attr_name: record.__dict__[attr_name]
        for attr_name in record.__dict__
        if attr_name not in BUILTIN_ATTRS
    }
