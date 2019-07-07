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
from pprint import pprint
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # to import util
from util.digNetwork.tcpclient import TcpClient
from util.digNetwork.tcpserver import TcpServer
from util.protocol import parse_request
from run_server import ServerConfig, load_config
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class DatasetExtractorServer():
    def __init__(self, config):
        self._noisy = config.get('verbose')
        from model_controller import ModelController
        self._tcp_server = TcpServer(config.ip, config.port, self.on_new_message, self.on_new_client, self.on_disconnect, max_conn=1, buffer_size=1024)
        self._is_waiting_next_frame = Event()
        self._model = ModelController(config, self._noisy)
        self._command = None
        self._commands = {}
        self._handle_unknown_command = self.cmd_unknown_command
        print('Server started')

    def print_if_noisy(self, item):
        if self._noisy:
            pprint(item, indent=2)

    def on_new_message(self, addr, data):
        '''
        Обработчик сообщений от клиента
        '''
        try:
            header, payload = parse_request(data)
            command = header['command']
        except Exception as ex:
            print("Invalid request: length: {}".format(len(data)))
            print("Exception: {}".format(ex))
            print("First 1000 bytes of request: ----------")
            print(data[:1000])
            print("---------------------------------------")
            self.send_error_reply(addr, 'application', 'generic_error', "Internal server error")
            return

        self._c_addr = addr
        self.print_if_noisy("--- New message from {}: -------------------------".format(addr))
        self.print_if_noisy(header)
        self._command = command
        self._c_header = header
        self._c_payload = payload
        self._is_waiting_next_frame.set()

    def on_new_client(self, addr):
        '''
        '''
        self._client_addr = addr
        return 0

    def on_disconnect(self, addr):
        pass

    def send_reply(self, client, response, event, success):
        response['event'] = event
        response['status'] = 'ok' if success else 'error'
        json_data = json.dumps(response)
        self.print_if_noisy('--- Sending response to {}:'.format(client))
        if len(json_data) <= 80:
            self.print_if_noisy(json_data)
        else:
            self.print_if_noisy(json.dumps(response, indent=2, sort_keys=True))
        self._tcp_server.send(client, json_data.encode())

    def cmd_load_image(self, client, header, payload):
        response = self._model.process_image(payload, header)
        response['frame_index'] = header['frame_index']
        self.send_reply(client, response, 'load_image', True)

    def cmd_ping(self, client, header, payload):
        self.send_reply(client, { 'message': 'pong' }, 'ping', True)

    def cmd_unknown_command(self, client, header, payload):
        command = header.get('command', '')
        message = "Command '{}' not recognized".format(command)
        self.send_error_reply(client, 'application', 'invalid_command', message, value=command)

    def send_error_reply(self, client, domain, code, message, **kwargs):
        self.send_reply(client, { 'message': message, 'domain': domain, 'code': code, **kwargs }, 'error', False)

    def register_command(self, name, handler):
        self._commands[name] = handler

    def work_loop(self):
        while True:
            try:
                self._is_waiting_next_frame.wait()
            except Exception:
                return
            try:
                handler = self._commands.get(self._command, self._handle_unknown_command)
                handler(self._c_addr, self._c_header, self._c_payload)
                self._is_waiting_next_frame.clear()
            except Exception as e:
                print("Exception: {}".format(e))
                self.send_error_reply(self._c_addr, 'application', 'generic_error', "Internal server error")
                self._is_waiting_next_frame.clear()
                continue

    def start(self):
        self.register_command('ping', self.cmd_ping)
        self.register_command('load_image', self.cmd_load_image)
        # NOTE: add other commands if needed
        self.work_thread = Thread(target=self.work_loop())
        self.work_thread.start()
        print('Server started')

    def stop(self):
        self._tcp_server.close()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Data analysis server')
    parser.add_argument('--ip', default='127.0.0.1', help="IP address of the interface to listen on (use 0.0.0.0 for all interfaces)")
    parser.add_argument('--port', default=1217, help="Server port", type=int)
    parser.add_argument('--config-file', default='config.json', help="Configuration file")
    parser.add_argument('--verbose', help="Show detailed debug messages", action='store_true')
    args = vars(parser.parse_args())
    config = load_config(ServerConfig, args.get('config_file'))
    config.update(args)

    print("Starting server on {}:{}".format(config.ip, config.port))
    server = DatasetExtractorServer(config)
    server.start()
    input("Press Enter to stop...")
    server.stop()
    input("Server stopped. Press Enter to continue...")

if __name__ == '__main__':
    main()
