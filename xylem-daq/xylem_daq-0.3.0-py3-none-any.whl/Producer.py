'''
The Producer component represents a data producer: one that accepts as
input certain commands, and that produces data as output.

'''
from __future__ import absolute_import
from __future__ import print_function
import zmq
import time

from .BaseComponent import BaseComponent, default_parameters
from . import protocol

class Producer(BaseComponent):
    def __init__(self, out_address, **kwargs):
        super_params = default_parameters()
        super_params['name'] = 'Producer'
        super_params['group'] = 'PRODUCER'
        super_params.update(kwargs)
        super_params['connect_addresses'] = {super_params['group']:
                out_address}
        super(Producer, self).__init__(**super_params)
        try:
            self.name_bytes = super_params['name'].encode('utf-8')
            self.out_socket = self.context.socket(zmq.PUB)
            self.sockets.append(self.out_socket)
            self.out_socket.bind(out_address)
        except:
            self.cleanup()
            raise

    def produce(self, data, metadata=None):
        '''
        Send the metadata and data to the next component in the network.

        '''
        if metadata is None:
            metadata = {}
        metadata.update({'name': self.name, 'timestamp': time.time()})
        message = protocol.data_create(metadata, data)
        self.out_socket.send_multipart(message)

    def send_info(self, message):
        '''
        Send an info message to the next component in the network.

        '''
        message = protocol.info_create(time.time(), self.name, message)
        self.out_socket.send_multipart(message)

