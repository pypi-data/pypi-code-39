import logging
import datetime
import socket
from cuculus import CuculusClient

local_hostname = socket.gethostname()
logLevels = {
    "DEBUG": 1,
    "INFO": 2,
    "WARNING": 3,
    "ERROR": 4,
    "CRITICAL": 5
}


class CuculusLoggingHandler(logging.Handler):
    def __init__(self,
                 client: CuculusClient,
                 app_id: str,
                 hostname: str = local_hostname):
        logging.Handler.__init__(self)
        self.client = client
        self.appId = app_id
        self.hostname = hostname

    def emit(self, record):
        try:
            data = {
                "AppId": self.appId,
                "Message": record.msg,
                "Logger": record.name,
                "Host": self.hostname,
                "Level": logLevels[record.levelname],
                "Timestamp": datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%dT%H:%M:%S.%fZ')
            }
            self.client.addLog(data)
        except Exception as ex:
            print(ex)
            pass
