import asyncio
import json
import logging
import websockets
from command_processor import CommandProcessor

async def send(client, message):
    await client.send(message)

async def broadcast(clients, message):
    if clients: # asyncio.wait doesn't accept an empty list
        await asyncio.wait([send(client, message) for client in clients])

class WebSocketServer:
    def __init__(self, name, config):
        self._name = name
        self._config = config
        self._processor = CommandProcessor(config)

    async def register(self, client):
        response = self._processor.add_client(client)
        if response:
            await send(client, response)

    def unregister(self, client):
        self._processor.remove_client(client)

    async def on_connect(self, client, path):
        # register(client) sends user_event() to client
        await self.register(client)
        try:
            while True:
                message = await client.recv()
                context = self._processor.process_message(client, message)
                response, keep_connection = self._processor.run_command(context)
                await send(client, response)
                if not keep_connection:
                    await client.close()
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print("Exception in WebSocketServer::on_connect:", e)
        finally:
            self.unregister(client)

    def start(self, ip, port, server_started):
        logging.basicConfig()
        asyncio.get_event_loop().run_until_complete(websockets.serve(self.on_connect, ip, port))
        server_started(self._name, ip, port)
        asyncio.get_event_loop().run_forever()