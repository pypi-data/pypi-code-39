# -*- coding: utf-8 -*-

import importlib
import os
import configparser
import asyncio
import asyncpg
import inspect
from functools import (partial, wraps)
from .action import Action
from .state import State
from qry import (Query, Id, Where)

attrs = {
    'grpc_server': None,
    'grpc_server_function': None,
    'grpc_host': '127.0.0.1',  # can be overwritten with config file
    'grpc_port': 50051  # can be overwritten with config file
}


def init(config_file='./config.ini'):

    if os.path.isfile(config_file) is True:
        config = configparser.ConfigParser()
        config.read(config_file)

    else:
        raise Exception(f"Config file {config_file} not found.")

    global _state
    _state = State(config)

    ioloop = asyncio.get_event_loop()
    _state.set_connection(
        ioloop.run_until_complete(
            asyncpg.create_pool(**config['POSTGRESQL'])
        )
    )

    if 'ACTIONS' in config.sections():
        for key in config['ACTIONS']:
            exec(f"""
{''}
def {key}(*arg, **args):
    act = _state.actions['{key}']
    ioloop = asyncio.get_event_loop()
    conn = None
    if _state.conn is not None:
        conn = ioloop.run_until_complete(
            _state.conn.acquire()
        )
    try:
        action = act(conn)
        result = ioloop.run_until_complete(
            action.process(*arg, **args)
        )
    finally:
        ioloop.run_until_complete(
            _state.conn.release(conn)
        )
    return result
            """, globals(), attrs)

    if 'SERVER' in config.sections() and 'server' in config['SERVER']:
        attrs['grpc_server'] = _state.import_action(
            config['SERVER']['server']
        )
        if 'client' in config['SERVER']:
            attrs['grpc_client'] = _state.import_action(
                config['SERVER']['client']
            )
        if 'host' in config['SERVER']:
            attrs['grpc_host'] = config['SERVER']['host']
        if 'port' in config['SERVER']:
            attrs['grpc_port'] = int(config['SERVER']['port'])


async def ainit(config_file='./config.ini'):

    if os.path.isfile(config_file) is True:
        config = configparser.ConfigParser()
        config.read(config_file)

    else:
        raise Exception(f"Config file {config_file} not found.")

    global _state
    _state = State(config)

    # Init database connection
    if 'POSTGRESQL' in config.sections():
        _state.set_connection(
            (
                await asyncpg.create_pool(**config['POSTGRESQL'])
            )
        )

    if 'SERVER' in config.sections() and 'server' in config['SERVER']:
        attrs['grpc_server'] = _state.import_action(
            config['SERVER']['server']
        )
        if 'client' in config['SERVER']:
            attrs['grpc_client'] = _state.import_action(
                config['SERVER']['client']
            )
        if 'host' in config['SERVER']:
            attrs['grpc_host'] = config['SERVER']['host']
        if 'port' in config['SERVER']:
            attrs['grpc_port'] = int(config['SERVER']['port'])
        
        # Create the GRPC Server Class
        methods = inspect.getmembers(
            attrs['grpc_server'],
            predicate=inspect.isfunction
        )

        attrs['grpc_server_function'] = []
        for method in methods:
            if method[0] != '__mapping__':
                attrs['grpc_server_function'].append(method[0])

    if 'ACTIONS' in config.sections():
        
        srv = """
class Server(attrs['grpc_server']):
    def __init__(self, easy):
        super().__init__()
        self.easy = easy
        """

        for key in config['ACTIONS']:
            exec(f"""
async def {key}(*arg, **args):
    act = _state.actions['{key}']

    if _state.conn is not None:
        async with _state.conn.acquire() as conn:
            action = act(conn)
            return (
                await action.process(*arg, **args)
            )
    else:
        action = act()
        return (
            await action.process(*arg, **args)
        )
        
            """, globals(), attrs)

        if (
            attrs['grpc_server'] is not None and
            attrs['grpc_server_function'] is not None
        ):
            for function in attrs['grpc_server_function']:
                if function in config['ACTIONS'].keys():
                    srv += f'''
    async def {function}(self, stream):
        f = await stream.recv_message()
        await stream.send_message(
            await self.easy.{function.lower()}(f)
        )
                    '''

                else:
                    srv += f'''
    async def {function}(self, stream):
        print("Not implemented")
        pass
                    '''

        exec(srv, globals(), attrs)

        # print(srv)


# PEP 562 (customization of module attribute access)
def __dir__():
    keys = [
        'Action',
        'init',
        'grpc_server',
        'Query',
        'Id',
        'Where'
    ] + list(attrs.keys())
    keys.sort()
    return keys


def __getattr__(key):
    return attrs.get(key)


def __setattr__(key, value):
    attrs[key] = value
