# -*- coding: utf-8 -*-
import logging
import logging.handlers

logging.basicConfig(filename="/tmp/novel.log", filemode="a+", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%Y-%m-%d %H:%M:%S %a", level=logging.INFO)

class Log(object):
    def log(self, logContent):
        if type(logContent) == str:
            logging.info(logContent)
        elif type(logContent) == unicode:
            logging.info(logContent.encode('utf-8'))
    def error(self, logContent):
        logging.error(logContent)
