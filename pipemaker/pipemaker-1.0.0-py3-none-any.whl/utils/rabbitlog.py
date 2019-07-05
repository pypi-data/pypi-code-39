# todo: change to fanout, create consumer that formats
from pipemaker.utils.rabbitq import Rabbitq
from pythonjsonlogger import jsonlogger
import logging

def json():
    """ formatter called by logging.yaml. format the log record columns in json format """
    return jsonlogger.JsonFormatter(reserved_attrs=[])

class Logq(Rabbitq):
    """ receive log messages from all processes
    """
    name = "log_queue"


class Rabbithandler(logging.Handler):
    """ logging handler that outputs to rabbit queue
    """
    def __init__(self):
        # note fails if use super()
        logging.Handler.__init__(self)
        self.q = Logq(heartbeat=0)

    def emit(self, record):
        msg = self.format(record)
        self.q.put(msg)