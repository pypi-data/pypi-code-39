# -*- coding: utf-8 -*-

import asyncio
import sys
from grpclib.server import Server
from grpclib.client import Channel
import easygrpc


async def start_server():
    loop = asyncio.get_running_loop()
    await easygrpc.ainit()

    server = Server([easygrpc.Server(easygrpc)], loop=loop)
    await server.start(easygrpc.grpc_host, easygrpc.grpc_port)

    print("Server ready.")

    try:
        await server.wait_closed()

    except asyncio.CancelledError:

        print("Closing server.")
        server.close()
        await server.wait_closed()

async def start_client():
    loop = asyncio.get_event_loop()
    await easygrpc.ainit()

    if easygrpc.grpc_client is None:
        print("Sorry, but you have not declared any client.")

    else:
        channel = Channel(easygrpc.grpc_host, easygrpc.grpc_port, loop=loop)
        await easygrpc.grpc_client(channel)
        channel.close()

if __name__ == '__main__':
    if '-client' in sys.argv or '-c' in sys.argv:
        asyncio.run(start_client())

    else:
        asyncio.run(start_server())
