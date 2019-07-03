#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
"""
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'

import requests
import json
import os
import socket
import sys
import threading
from datetime import datetime
from time import time, sleep

from keychest_agent.core import Core
from keychest_agent.config import KCConfig
from keychest_agent.logger import logger


class LogDispatcher(threading.Thread):

    def __init__(self, stop_event, sock_file='logbook.sock', ip=None, port=0):
        """
        :param stop_event:
        :param sock_file: the TCP .sock file for listening
        :param ip: or we can listen on an interface and ...
        :param port: ... tcp port
        """
        super().__init__()
        self.stopping = False
        self.messages = []
        self.stop_event = stop_event  # type: threading.Event
        self.stopped = False

        if ip is not None:
            self.sock_address = (ip, port)
            self.sock_type = socket.AF_INET
        else:
            self.sock_type = socket.AF_UNIX
            self.sock_address = \
                os.path.join(KCConfig.config.sockdir, sock_file)
            # first we need to create a .sock file for internal communication
            try:
                os.unlink(self.sock_address)
            except OSError:
                if os.path.exists(self.sock_address):
                    raise

        self.code_dir = Core.get_custom_config_file_path('etc/keychest_agent/log_codes.pickle')
        # first, let's empty the queue
        self.myindex = None

    def tcp_server(self):
        """
        This is internal TCP  server for logging - it listens on localhost
        :return:
        """

        while True:
            serv_socket = socket.socket(self.sock_type, socket.SOCK_STREAM)
            try:
                serv_socket.bind(self.sock_address)
            except Exception as ex:
                sys.stdout.write("Can't bind to logging socket: %s" % str(ex))

            try:
                serv_socket.listen(1)
                while True:
                    # Wait for a connection
                    connection, client_address = serv_socket.accept()
                    end_of_data = False
                    data = ""
                    try:
                        while not end_of_data:
                            data += connection.recv(10000).decode()
                            if data:
                                # process data - look for end of line
                                _lines = data.split(os.linesep)
                                # if data ends with os.linesep -> list item will be empty string
                                length = 0
                                for _line in _lines:
                                    length = len(_line)
                                    if length > 0:
                                        self.messages.append(_line)
                                if length > 0:
                                    data = _lines[len(_lines) - 1]  # store the last one
                                else:
                                    data = ''
                            else:
                                # no more data
                                end_of_data = True
                    finally:
                        connection.close()
            except Exception as ex:
                sys.stdout.write("Exception in listening to logging port %s" % str(ex))

    def run(self):
        """

        :return:
        """

        # first we need to start the TCP server to accept logs
        tcp_server = threading.Thread(target=self.tcp_server, args=())
        tcp_server.name = "TCPHandler"
        tcp_server.daemon = True  # let it terminate with the main thread
        tcp_server.start()

        # splunk - not now

        # mysocket = None
        # splunk_port = 8089
        # splunk_host = 'localhost'
        # splunk_password = 'password'
        # splunk_user = 'admin'
        # try:
        #     KCConfig.config.logging_host = urllib.parse.quote_plus(socket.gethostname().replace(".", "_"))
        #     loggin_splunk = KCConfig.config.logging_splunk
        #     connection_details = loggin_splunk.split(",")
        #     if len(connection_details) == 1:
        #         splunk_password = connection_details[0]
        #     elif len(connection_details) < 3:
        #         splunk_user = connection_details[0]
        #         splunk_password = connection_details[1]
        #     elif len(connection_details) < 4:
        #         splunk_user = connection_details[0]
        #         splunk_password = connection_details[1]
        #         splunk_host = connection_details[2]
        #     elif len(connection_details) > 3:
        #         splunk_user = connection_details[0]
        #         splunk_password = connection_details[1]
        #         splunk_host = connection_details[2]
        #         try:
        #             splunk_port = int(connection_details[3])
        #         except ValueError:
        #             pass
        #     splunk_ep = sclient.connect(
        #         host=splunk_host,
        #         port=splunk_port,
        #         username=splunk_user,
        #         password=splunk_password
        #     )
        #
        #     existing_indexes = splunk_ep.indexes
        #     create = True
        #     for index in existing_indexes:
        #         if index.name == KCConfig.config.logging_index:
        #             create = False
        #     if create:
        #         splunk_ep.indexes.create(KCConfig.config.logging_index)
        #
        #     self.myindex = splunk_ep.indexes[KCConfig.config.logging_index]
        #     mysocket = self.myindex.attach(sourcetype='keychest', host=KCConfig.config.logging_host)
        #
        # except Exception as ex:
        #     # splunk_ep = None
        #     sys.stdout.write("Can't open splunk connection %s" % str(ex))
        #     sys.stdout.flush()

        agent_email = KCConfig.config.agent_email  # type: str
        if agent_email.startswith("dummy"):
            registered = False
        else:
            registered = True

        logger.load_codes(self.code_dir)
        last_submit = time()
        upload_string = []  # this would be "" for splunk!
        last_reconnect = time()
        usage_logs_counter = 0
        last_config_test = time()
        while True:
            # noinspection PyBroadException
            try:
                if not registered:
                    if time() - last_config_test > 10:  # retry no more than every 10 seconds
                        if agent_email != KCConfig.config.agent_email:
                            agent_email = KCConfig.config.agent_email  # type: str

                        if not agent_email.startswith("dummy"):
                            registered = True
                        else:
                            registered = False
                        last_config_test = time()

                if len(self.messages) > 0:
                    record = self.messages.pop(0)  # take the oldest message
                    skip = False
                    # noinspection PyBroadException
                    try:
                        raw = json.loads(record)
                        level = raw['level'].upper()
                        # flag whether it's a trace or usage log message
                        if 'usage' in raw:
                            usage = raw['usage']
                        else:
                            usage = False
                        if usage:
                            level = 'USE'
                            usage_logs_counter = (usage_logs_counter + 1) % KCConfig.config.logging_usage_sampling
                            skip = (usage_logs_counter != 0)

                        if 'params' in raw:
                            params = raw['params']
                        else:
                            params = "{}"

                        if 'code' in raw:
                            code, msg_id = logger.get_code(level, raw['code'], raw['message'])
                        else:
                            code, msg_id = logger.get_code(level, None, raw['message'])

                        _time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
                        _params = json.loads(params)
                        if len(self.messages) > 50:
                            _params['backlog'] = len(self.messages)
                        _message = {'time': raw['time'][:19],
                                    'agent': agent_email,
                                    'event':
                                        {
                                            'level': level,
                                            'code': code,
                                            'message': raw['message'],
                                            'params': _params,
                                            'process': raw['process'],
                                            'id': msg_id,
                                            'host': raw['host'],
                                            'usage': usage,
                                            'git': KCConfig.config.git_version,
                                            'log_time': _time,
                                        }
                                    }
                        message = json.dumps(_message) + os.linesep

                        # if logging_keychest and (time() - last_reconnect > 60):
                        #     if mysocket is None or self.myindex is None and (time() - last_reconnect > 60):
                        #         # don't try to reconnect more often than once a minute
                        #         try:
                        #             last_reconnect = time()
                        #             splunk_ep = sclient.connect(
                        #                 host=splunk_host,
                        #                 port=splunk_port,
                        #                 username=splunk_user,
                        #                 password=splunk_password
                        #             )
                        #             if self.myindex is None:
                        #                 self.myindex = splunk_ep.indexes[KCConfig.config.logging_index]
                        #             if mysocket is None:
                        #                 mysocket = self.myindex.attach(sourcetype='keychest', host=KCConfig.config.logging_host)
                        #         except Exception as ex:
                        #             # splunk_ep = None
                        #             sys.stdout.write("Can't open splunk connection %s" % str(ex))
                        #             sys.stdout.flush()
                        #     pass

                        # if (not skip) and (level in KCConfig.config.logging_remote) and self.myindex and mysocket:
                        if (not skip) and (level in KCConfig.config.logging_remote) and registered:
                            resp = None
                            try:
                                upload_string.append(_message)  # we need JSON here
                                if time() - last_submit > 1:  # every 1 seconds
                                    data = {
                                        'agent': agent_email,
                                        "timestamp": int(time()),
                                        "security": "none",
                                        "signature": None,
                                        "logs": upload_string
                                    }
                                    # add customer-defined items
                                    if isinstance(KCConfig.config.logging_params, dict):
                                        for key, param in KCConfig.config.logging_params.items():
                                            if key not in data:
                                                data[key] = param

                                    headers = {'Accept': 'application/json'}
                                    resp = requests.post(KCConfig.config.logging_server, json=data, headers=headers)
                                    last_submit = time()

                                    upload_string = []
                            except Exception as ex:
                                cause = str(ex)
                                code = 0 if resp is not None else resp.status_code
                                sys.stdout.write("Error posting logs to a remote server %s - %s, code: %r" %
                                                 (KCConfig.config.logging_server,  cause, code))
                                upload_string = []
                                # self.myindex = None
                                # mysocket = None

                        # local log
                        if level in KCConfig.config.logging_local:
                            sys.stdout.write(message)
                    except Exception:
                        pass
                else:  # i.e., the queue is empty
                    sleep(0.5)
                    if self.stop_event.is_set():
                        break
            except Exception as ex:
                pass
        # noinspection PyUnreachableCode
        sys.stdout.write("Terminating log dispatcher" + os.linesep)
        self.stopped = True

    def stop(self):
        self.stop_event.set()
        while not self.stopped:
            sleep(0.5)
