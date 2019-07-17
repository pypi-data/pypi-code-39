'''
A logging module.

'''
from __future__ import print_function
from __future__ import absolute_import
import logging
from datetime import datetime

import zmq

import xylem.protocol as protocol

class LogCollector(object):
    '''
    Collect log messages from xylem components and save them to disk.

    '''
    LEVELS = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
            }

    def __init__(self, port, filename):
        self.port = port
        self.filename = filename
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename)
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(message)s')
        self.handler.setFormatter(self.formatter)
        self.stderr_handler = logging.StreamHandler()
        self.stderr_handler.setLevel(logging.INFO)
        self.stderr_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.addHandler(self.stderr_handler)
        self.context = zmq.Context()


    def run(self):
        try:
            self.receiver = self.context.socket(zmq.SUB)
            self.receiver.setsockopt(zmq.SUBSCRIBE, b'')
            self.receiver.bind(self.port)
            while True:
                message_raw = self.receiver.recv_multipart()
                parsed_message = protocol.log_parse(message_raw)
                timestamp = parsed_message['metadata']['timestamp']
                component = parsed_message['metadata']['component']
                message = parsed_message['message']
                level = self.LEVELS[parsed_message['metadata']['level']]
                self.logger.log(level, '%s | %-8s | %-20s | %s',
                        datetime.fromtimestamp(timestamp).isoformat(' '),
                        parsed_message['metadata']['level'],
                        component, message)
        finally:
            self.receiver.close(linger=0)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port')
    parser.add_argument('-o', '--output', help='The log file destination')
    args = parser.parse_args()
    logger = LogCollector(args.port, args.output)
    try:
        logger.run()
    except KeyboardInterrupt:
        pass
