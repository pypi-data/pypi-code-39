'''
The Aggregator component collects data from data producers and
broadcasts it to data consumers.

'''
from __future__ import absolute_import
from __future__ import print_function
import zmq
from .BaseComponent import BaseComponent, default_parameters
from . import protocol

class Aggregator(BaseComponent):
    def __init__(self, out_address, **kwargs):
        super_params = default_parameters()
        super_params['name'] = 'Aggregator'
        super_params['group'] = 'AGGREGATOR'
        super_params.update(kwargs)
        super_params['connect_addresses'] = {super_params['group']:
                out_address}
        super(Aggregator, self).__init__(**super_params)
        try:
            self.in_socket = self.context.socket(zmq.SUB)
            self.sockets.append(self.in_socket)
            for connection in self.connections:
                self.in_socket.connect(self.addresses[connection])
            self.in_socket.setsockopt_string(zmq.SUBSCRIBE, u'')
            self.poller.register(self.in_socket, zmq.POLLIN)
            self.handlers[self.in_socket] = self.handle_in_socket
            self.out_socket = self.context.socket(zmq.PUB)
            self.sockets.append(self.out_socket)
            self.out_socket.bind(out_address)
        except:
            self.cleanup()
            raise

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
                handler.handl(self.name, header, info_message)
            return 'INFO', header, info_message

    def broadcast(self, metadata, data):
        message = protocol.data_create(metadata, data)
        self.out_socket.send_multipart(message)

    def rebroadcast_info(self, header, message):
        message_list = protocol.info_create(header['timestamp'],
                header['component'], message)
        self.out_socket.send_multipart(message_list)

    def broadcast_info(self, message):
        message_list = protocol.info_create(time.time(), self.name, message)
        self.out_socket.send_multipart(message_list)

