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

Created on Thu Aug 30 20:06:37 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Thu Aug 30 20:42:30 2018'
__version__ = '0.1'

import socket
from threading import Thread
from digNetwork.tcpbase import TcpBase


class TcpServer(TcpBase):
    '''
    handlers:
        <on_message>(addr, data)
        <on_new_client>(addr)
    '''
    def __init__(self,
                 ip,
                 port,
                 on_message,
                 on_new_client,
                 on_disconnect,
                 max_conn=10,
                 buffer_size=1024):
        self._ip = ip
        self._port = port
        self._on_message = on_message
        self._on_new_client = on_new_client
        self._on_disconnect = on_disconnect
        self._max_conn = max_conn
        self._client_connections = {}  # Соединения с клиентами
        self._recieve_threads = {}  # Потоки-обработчики сообщений от клиентов
        self._buffer_size = buffer_size

        self._socket = socket.socket()
        self._socket.bind((self._ip, self._port))
        self._socket.listen(self._max_conn)

        # init threads
        self._work_loop_thread = Thread(target=self._work_loop,
                                        args=(self._socket, ))
        self._work_loop_thread.start()

    def _recieve_data(self, connection, addr, buffer):
        self._on_new_client(addr)
        while connection is not None:
            try:
                data = self.recv_msg(connection)
                self._on_message(addr, data)
            except Exception:
                print("Connection was closed by peer")
                if connection is not None:
                    self.disconnect_client(addr)
                    connection = None
        return

    def _work_loop(self, m_socket):
        while m_socket:
            conn, addr = m_socket.accept()
            print("New client: {}".format(addr))
            self._client_connections[addr] = conn
            new_thread = Thread(target=self._recieve_data,
                                args=(conn, addr, self._buffer_size))
            new_thread.start()
            self._recieve_threads[addr] = new_thread
        print("Exit from work loop")
        return

    def disconnect_client(self, addr):
        '''
        Disconnect from client
        '''
        conn = self._client_connections.pop(addr, None)
        if conn is not None:
            conn.close()
            conn = None
        self._on_disconnect(addr)
        self._recieve_threads.pop(addr, None)

    def send(self, addr, data):
        '''
        Send raw data to client addr
        '''
        try:
            self.send_msg(self._client_connections[addr], data)
        except Exception as e:
            print("Packet did not reach destination")
            print("Exception: {}".format(e))

    def close(self):
        '''
        Close all connection and stop TCP server
        '''
        for conn in self._client_connections:
            if conn is not None:
                conn[1].close()
        for thread in self._recieve_threads:
            if thread is not None:
                thread[1].join()


def on_message_handler_example(addr, data):
    '''
    Example callback for new message event
    '''
    print("Recieve from {}: {}".format(addr, data.decode()))
    server.send(addr, data)


def on_new_client_example(addr):
    '''
    Example callback for new client event
    '''
    print("New client: {}".format(addr))


if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = 1234
    print("Starting server on {}:{}".format(IP, PORT))
    server = TcpServer(IP,
                       PORT,
                       on_message_handler_example,
                       on_new_client_example)
    input("Press Enter to continue...")
    server.close()
