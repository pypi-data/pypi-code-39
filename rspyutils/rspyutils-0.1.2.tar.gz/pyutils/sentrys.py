# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@version: 0.1
@author: gabriel
@file: sentrys.py
@time: 2018/11/20 15:12
"""
from raven import Client


class SentryClient(object):
    def __init__(self, config):
        DSN = config.get("Sentry_dsn",None)
        if DSN:
            self.client = Client(DSN)
        else:
            raise Exception("Sentry_dsn input error!!!")

    def check_commom_err(self, e):
        self.client.captureException(e)
