# coding: utf-8

from __future__ import print_function

import zmq


class Client(object):
    def __init__(self, port, host='localhost', verbose=0):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(host, port))
        if verbose > 0:
            print('writing to:', port)

    def send_recv(self, msg, verbose=False):
        if verbose:
            print('>>rbc>>', msg)
        self.socket.send_string(msg)
        result = self.socket.recv_string()
        if verbose:
            print('<<rbc<<', result)
        return result
