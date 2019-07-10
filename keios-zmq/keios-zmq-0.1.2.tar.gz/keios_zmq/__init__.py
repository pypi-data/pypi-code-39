import asyncio
import logging
from typing import Callable

import zmq

logging.basicConfig(level=logging.INFO)


class KeiosZMQ:
    """
    server wrapper for keios implementations
    TODO: refactor to threadpool based implementation
    """
    logger = logging.getLogger("keios-py-zmq-connector")

    def __init__(self, port: int, message_handler: Callable[[bytearray], bytearray]):
        self._zmq_context = zmq.Context()
        self._socket = self._zmq_context.socket(zmq.ROUTER)
        self._socket.bind("tcp://*:{}".format(port))
        self._message_handler = message_handler
        self.stopped = False

    async def internal_handler(self):
        while not self.stopped:
            try:
                addr, msg = await self.internal_receive_message()
                self.logger.debug("msg received - identity: {}, data: {}".format(addr, msg))
                await self.internal_send_message(addr, self._message_handler(msg))
            except zmq.error.ContextTerminated as e:
                pass  # this error is expected from .close()

    async def internal_receive_message(self):
        """
        Wraps blocking zmq recv
        :return:
        """
        identity, data = self._socket.recv_multipart()
        return [identity, data]

    async def internal_send_message(self, identity, message):
        return self._socket.send_multipart([identity,
                                            message])

    def start_server(self, loop=None):
        if loop is None:
            self.event_loop = asyncio.get_event_loop()
        else:
            self.event_loop = loop
        try:
            self.event_loop.run_until_complete(asyncio.wait([
                self.internal_handler()
            ]))
        except RuntimeError as e:
            pass  # this error is expected from .close()

    def close(self):
        self.stopped = True
        self.event_loop.stop()
