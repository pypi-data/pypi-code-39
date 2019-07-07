#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Wed Oct 24 18:58:55 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Created on Wed Oct 24 18:58:55 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'Proprietary'
__date__ = 'Wed Oct 24 18:58:55 2018'
__version__ = '0.1'

import os
import sys
import json
from threading import Thread, Event
from datetime import datetime

from util.digNetwork.tcpclient import TcpClient
from util.digNetwork.tcpserver import TcpServer
from util.protocol import parse_request
from util.config import TCP_SERVER_MAX_CONN, TCP_SERVER_BUFFER_SIZE
from command_processor import CommandProcessor

class CustomTCPServer():
    def __init__(self, name, config):
        self._name = name
        self._config = config
        self._processor = CommandProcessor(config)

    def on_new_client(self, client):
        response = self._processor.add_client(client)
        self._tcp_server.send(client, response)

    def on_new_message(self, client, data):
        self._context = self._processor.process_message(client, data)
        self._is_waiting_next_frame.set()

    def start(self, ip, port, served_started):
        self._is_waiting_next_frame = Event()
        self._tcp_server = TcpServer(ip, port,
            self.on_new_message, self.on_new_client, self._processor.remove_client,
            max_conn=self._config.tcp_server_max_conn, buffer_size=self._config.tcp_server_buffer_size)
        self.work_thread = Thread(target=self.work_loop)
        self.work_thread.start()
        served_started(self._name, ip, port)

    def work_loop(self):
        while True:
            try:
                self._is_waiting_next_frame.wait()
                response, keep_connection = self._processor.run_command(self._context)
                self._tcp_server.send(self._context.client, response)
                if not keep_connection: pass # TODO: close connection
            except Exception as e:
                print("Exception in work_loop: {}".format(e))
            finally:
                self._is_waiting_next_frame.clear()