import asyncio
import websockets
from threading import Thread

class WebSocketClient:
    def __init__(self, server_ip, server_port, on_connect, on_message):
        self._server_ip = server_ip
        self._server_port = server_port
        self._on_message = on_message
        self._on_connect = on_connect
        self._task = None
        self._websocket = None

    def _recieve_data(self):
        async def main_task():
            async with websockets.connect( 'ws://{}:{}'.format(self._server_ip, self._server_port)) as websocket:
                self._websocket = websocket
                self._on_connect(self._server_ip, self._server_port)
                try:                
                    while True:
                        # print('Checking for messages')
                        message = await websocket.recv()
                        # print("Received message:", message)
                        self._on_message(message)
                except asyncio.CancelledError:
                    # print("Websocket task canceled")
                    pass
                except Exception as ex:
                    print("Exception in websocket thread:", ex)

        self._loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._task = loop.create_task(main_task())
        loop.run_until_complete(self._task)

    def start(self):
        self._receive_thread = Thread(target=self._recieve_data)
        self._receive_thread.start()

    async def send_async(self, data):
        await self._websocket.send(data)
        # print('Sent {} bytes to {}'.format(len(data), (self._server_ip, self._server_port)))

    def send(self, data):
        '''
        Send raw data to server
        '''
        asyncio.run_coroutine_threadsafe(self.send_async(data), self._loop)

    async def cancel_task(self):
        self._task.cancel()

    def close(self):
        '''
        Close tcp client
        '''
        try:
            asyncio.run_coroutine_threadsafe(self.cancel_task(), self._loop)
            self._receive_thread.join(0.3)
        except:
            pass