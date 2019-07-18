'''
The Consumer component represents a data consumer: one that accepts data
as input and does not produce any output (at least not onto the
network).

'''
from __future__ import absolute_import
from __future__ import print_function
import zmq
import time

from .BaseComponent import BaseComponent, default_parameters
from . import protocol

class Consumer(BaseComponent):
    def __init__(self, **kwargs):
        super_params = default_parameters()
        super_params['name'] = 'Consumer'
        super_params['group'] = 'CONSUMER'
        super_params.update(kwargs)
        super(Consumer, self).__init__(**super_params)
        try:
            self.in_socket = self.context.socket(zmq.SUB)
            self.sockets.append(self.in_socket)
            for connection in self.connections:
                self.in_socket.connect(self.addresses[connection])
            self.in_socket.setsockopt_string(zmq.SUBSCRIBE, u'')
            self.handlers[self.in_socket] = self.handle_in_socket
            self.poller.register(self.in_socket, zmq.POLLIN)
        except:
            self.cleanup()
            raise

    def addHandler(self, handler):
        '''
        Add the given event handler.

        '''
        event = handler.event
        self._event_handlers[event].append(handler)

    def handle_in_socket(self):
        message_list = self.in_socket.recv_multipart()
        if message_list[0] == b'DATA':
            message = protocol.data_parse(message_list)
            data = message['data']
            metadata = message['header']
            for handler in self._event_handlers['data_message']:
                handler.handle(self.name, metadata, data)
            return 'DATA', metadata, data
        elif message_list[0] == b'INFO':
            message = protocol.info_parse(message_list)
            header = message['header']
            info_message = message['message']
            for handler in self._event_handlers['info_message']:
                handler.handle(self.name, header, info_message)
            return 'INFO', header, info_message

