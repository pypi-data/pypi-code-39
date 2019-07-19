#!/usr/bin/env python
# encoding: utf-8

import sys
import logging
from typing import Union
from openbayestool.jwt_client import JwtClient
from datetime import datetime

Number = Union[int, float]
Param = Union[int, float, str]

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class Updater:
    def __init__(self, jwt_client: JwtClient, callback_url: str=None):
        self.jwt_client = jwt_client
        self.callback_url = callback_url

    def set_access_token(self, token):
        self.jwt_client.set_token(token)

    def get_access_token(self):
        return self.jwt_client.token

    def set_callback_url(self, callback_url):
        self.callback_url = callback_url

    def get_callback_url(self):
        return self.callback_url

    def log_metric(self, key: str, value: Number):
        if not isinstance(value, (int, float)):
            print("WARNING: The metric {}={} was not logged because the value is not a number.".format(key, value),
                  file=sys.stderr)
            return

        if self.callback_url is None:
            print("WARNING: No callback url is given", file=sys.stderr)
            return

        self.jwt_client.put(self.callback_url, json={
            'metrics': {
                key: [{
                    'value': value,
                    'created_at': datetime.now().isoformat()
                }]
            }
        })

    def log_param(self, key: str, value: Param):
        if not isinstance(value, (int, float, str)):
            print("WARNING: The param {}={} was not logged because the value is not a number.".format(key, value),
                  file=sys.stderr)
            return

        if self.callback_url is None:
            print("WARNING: No callback url is given", file=sys.stderr)
            return

        self.jwt_client.put(self.callback_url, json={
            'parameters': {
                key: value
            }
        })
