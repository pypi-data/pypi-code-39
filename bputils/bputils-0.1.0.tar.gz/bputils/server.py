import asyncio
import logging
import os
import signal
import sys
from dataclasses import _MISSING_TYPE
from typing import List

from dotenv import load_dotenv
from grpclib.server import Server as AsyncServer

logger = logging.getLogger("grpc-server")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def build_env(env_dataclass, log=logger):
    def is_required(field):
        return type(field.default) == _MISSING_TYPE and type(field.default_factory) == _MISSING_TYPE

    load_dotenv()

    config_fields = [k for k, v in env_dataclass.__dataclass_fields__.items()]
    required_config_fields = [k for k, v in env_dataclass.__dataclass_fields__.items() if is_required(v)]

    if [log.error(f'{fname} environment is required')
        for fname in required_config_fields if fname not in os.environ or not os.environ[fname]]:
        sys.exit(1)

    [log.warning(f'{fname} environment is not set')
     for fname in config_fields if fname not in os.environ or not os.environ[fname]]

    return env_dataclass(**{k: os.environ.get(k) for k in config_fields if os.environ.get(k)})


def start_async_grpc_server(services: List, host: str, port: int, log=logger):
    loop = asyncio.get_event_loop()
    server = None

    try:
        server = AsyncServer(services, loop=asyncio.get_event_loop())

        log.info(f"Running grpc server: {host}:{port}...")
        loop.run_until_complete(server.start(host, port))

        stop = asyncio.Future()
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
        loop.run_until_complete(stop)

    except KeyboardInterrupt:
        log.info("...trying to graceful shutdown...")

    finally:
        server and server.close()
        server and loop.run_until_complete(server.wait_closed())
        log.info("\n...grpc server shutdown complete.")
