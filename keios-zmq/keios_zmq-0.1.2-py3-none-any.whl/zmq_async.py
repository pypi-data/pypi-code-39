import zmq
import threading
from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("keios-py-async-zmq-connector")

class AsyncMessageHandler(threading.Thread, ABC):
    def __init__(self, context, address):
        threading.Thread.__init__(self)
        self.context = context
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.bind(address)

    def run(self):
        try:
            while True:
                multipart = self.socket.recv_multipart()
                logger.debug(f'{self.__class__.__name__} received {multipart}')
                response = None
                response = self.handle(multipart[1], multipart[2])
                if response is None:
                    pass
                else:
                    multipart[-1] = response
                    self.socket.send_multipart(multipart)
                    logger.debug(f'{self.__class__.__name__} sent {response} to client {multipart[1]}')
        except zmq.error.ContextTerminated as e:
            pass # this error is expected from .close()

    @abstractmethod
    def handle(self, identity, message):
        """
        Returning none means to not respond at all.
        """

    def close(self):
        self.context.term()
        self.socket.close()

class AsyncKeiosZMQServer(threading.Thread):
    def __init__(self, handler=AsyncMessageHandler, port=4242):
        threading.Thread.__init__(self)
        backend_address = 'inproc://backend'
        self.context = zmq.Context()
        self.handler = handler(self.context, backend_address)
        self.handler.start()
        self.backend = self.context.socket(zmq.DEALER)
        self.backend.connect(backend_address)
        self.receiver = self.context.socket(zmq.ROUTER)
        self.receiver.bind(f'tcp://*:{port}')
        self.stop_running = False

    def run(self):
        poller = zmq.Poller()
        poller.register(self.backend, zmq.POLLIN)
        poller.register(self.receiver, zmq.POLLIN)
        try:
            while not self.stop_running:
                socks = dict(poller.poll())
                if self.backend in socks:
                    multipart = self.backend.recv_multipart()
                    self.receiver.send_multipart(multipart)
                    logger.debug(f'{self.__class__.__name__} sent {multipart} to client')
                if self.receiver in socks:
                    multipart = self.receiver.recv_multipart()
                    self.backend.send_multipart(multipart, copy=False)
                    logger.debug(f'{self.__class__.__name__} sent {multipart[1]} to backend')
        except zmq.error.ContextTerminated as e:
            pass # this error is expected from .close()

    def close(self):
        self.stop_running = True


class AsyncKeiosZMQClient(threading.Thread, ABC):
    def __init__(self, name=None, address='localhost', port=4242, timeout=100):
        threading.Thread.__init__(self)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        if name is not None:
            name = bytes(name, encoding='utf-8')
            self.socket.setsockopt(zmq.IDENTITY, name)
        self.socket.connect(f'tcp://{address}:{port}')
        self.timeout = timeout
        self.stop_sending = False
        self.stop_receiving = False

    def run(self):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)
        try:
            while not self.stop_sending:
                message = self.handle_send()
                self.socket.send(message)
                logger.debug(f'{self.__class__.__name__} sent {message}')
                sockets = dict(poll.poll(self.timeout))
                if self.socket in sockets:
                    message = self.socket.recv()
                    self.handle_receive(message)
                    logger.debug(f'{self.__class__.__name__} received {message}')
            while not self.stop_receiving:
                sockets = dict(poll.poll())
                if self.socket in sockets:
                    message = self.socket.recv()
                    self.handle_receive(message)
                    logger.debug(f'{self.__class__.__name__} received {message}')
        except zmq.error.ZMQError as e:
            pass # this error is expected from .close()

    @abstractmethod
    def handle_send(self):
        pass

    @abstractmethod
    def handle_receive(self, message):
        pass

    def close(self):
        self.stop_sending = True
        self.stop_receiving = True