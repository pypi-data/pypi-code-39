import asyncio
import socketio
from serve import rpc, exported, rpc_serve
from stub import get_service_proxy

@rpc()
class ClientSideService:
    @exported
    def mul(self, a, b):
        print('mul', a, b)
        return a * b

async def test_func(sio, service):
    print('run test_func')
    print(await service.add(1, 2))
    print(await service.addAsync(1, 2))

    try:
        await service.throwError()
    except Exception as e:
        print(e)

    try:
        await service.sub(1, 2)
    except Exception as e:
        print(e)

    await service.callClientMul()
    print('done !!!')
    await sio.disconnect()


async def main():
    sio = socketio.AsyncClient()
    print('connecting')
    await sio.connect('ws://localhost:3333')
    service = get_service_proxy(sio, 'ServerSideService')
    rpc_serve(sio, ClientSideService())
    await asyncio.gather(
        sio.wait(),
        test_func(sio, service)
    )

asyncio.run(main())
