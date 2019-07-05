# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Thu Aug 30 20:42:58 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""
__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Thu Aug 30 20:42:58 2018'
__version__ = '0.2'

import socket
from threading import Thread, Event
from util.digNetwork.tcpbase import TcpBase


class TcpClient(TcpBase):
    '''
        on_message(data)
    '''
    def __init__(self,
                 server_ip,
                 server_port,
                 on_connect,
                 on_message,
                 buffer_size=1024):
        self._server_ip = server_ip
        self._server_port = server_port
        self._buffer_size = buffer_size
        self._on_message = on_message
        self._on_connect = on_connect
        self._client_socket = None
        self._stop_event = None

    def _recieve_data(self, buffer):
        while not self._stop_event.is_set():
            # print('Checking for messages')
            try:
                data = self.recv_msg(self._client_socket)
            except socket.timeout:
                continue
            if data is not None:
                # print("Recieve msg with {} bytes".format(len(data)))
                self._on_message(data)
        self._client_socket.close()

    def start(self):
        self._stop_event = Event()
        self._client_socket = socket.socket()
        # Timeout in seconds to wait until a message is received in a single loop iteration
        self._client_socket.settimeout(10) 
        self._client_socket.connect((self._server_ip, self._server_port))
        self._on_connect(self._server_ip, self._server_port)
        self._receive_thread = Thread(target=self._recieve_data, args=(self._buffer_size,))
        self._receive_thread.start()

    def send(self, data):
        '''
        Send raw data to server
        '''
        self.send_msg(self._client_socket, data)
        # print('Sent {} bytes to {}'.format(len(data), (self._server_ip, self._server_port)))

    def close(self):
        '''
        close tcp client
        '''
        try:
            self._stop_event.set()
            self._client_socket.shutdown(socket.SHUT_WR)
            self._receive_thread.join(0.1)
        except:
            pass

def on_message_handler_example(data):
    '''
    Expample callback for tcp client massage receiving
    '''
    print("Recieve: {}".format(data.decode()))


if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = 1234
    print("Starting client to {}:{}".format(IP, PORT))
    client = TcpClient(IP, PORT, on_message_handler_example)
    cmd = 'a'
    while cmd != 'q':
        client.send(cmd.encode())
        cmd = input("Input some string to continue OR q + Enter for exit...")

    input("Press Enter to continue...")
    client.close()
