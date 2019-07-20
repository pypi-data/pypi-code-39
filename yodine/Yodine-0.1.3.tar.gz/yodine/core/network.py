from .entity import Manager, Component, Entity
from .vector import Vector
from typing import Callable

import uuid
import socket
import trio
import pyglet

try:
    import simplejson as json

except ImportError:
    import json



def dump_arg(arg):
    if isinstance(arg, Vector):
        return { 'type': 'vec', 'coord': [arg.x,arg.y] }

    elif isinstance(arg, Component):
        return { 'type': 'component', 'eid': arg.entity.id, 'name': arg.name, 'value': arg.value }

    elif isinstance(arg, Entity):
        return { 'type': 'entity', 'eid': arg.id }

    elif isinstance(arg, pyglet.window.Window):
        return { 'type': 'window' }

    return { 'type': 'normal', 'value': arg }


class Client(object):
    def __init__(self, manager: Manager, server_addr):
        self.manager = manager
        self.client = socket.create_connection(server_addr)
        self.client.setblocking(False)
        self.addr = server_addr
        self.players = {}
        self.events = []

    def send_event(self, data):
        source, name, args, kwargs = data

        if source.has('player', 'localplayer', 'name'):
            self._write('\x00'.join(['EVENT', *(json.dumps(dump_arg(a)) for a in [source['name'].value, name, *args])]).encode('utf-8') + b'\n')

    def stop(self):
        self._write(b'LEAVE\n')
        self.client.close()

    def load_arg(self, arg):
        if arg['type'] == 'vec':
            return Vector(arg['coord'])

        elif arg['type'] == 'normal':
            return arg['value']

        elif arg['type'] == 'component':
            c = self.manager.find_entity(arg['eid'])[arg['name']]
            c.value = arg['value']
            return c

        elif arg['type'] == 'entity':
            return self.manager.find_entity(arg['eid'])

        elif arg['type'] == 'window':
            return self.manager.window
        
        else:
            raise ValueError("Unknown JSON argument type: {}".format(repr(arg['type'])))

    def _write(self, data):
        self.outbound += data

    async def run(self):
        self.buffer = b''
        self.outbound = b''

        player = None

        for p in self.manager:
            if 'localplayer' in p:
                player = p
                break

        @self.manager.global_listener
        def broadcast_event(source, name, *args, **kwargs):
            if self.events is not None:
                self.events.append((source, name, args, kwargs))

            else:
                self.send_event((source, name, args, kwargs))

        async def _recv(data):
            self.buffer += data
            lines = self.buffer.split(b'\n')
            self.buffer = lines[-1]

            for data in lines[:-1]:
                try:
                    data = data.decode('utf-8')

                except UnicodeDecodeError:
                    print(data)
                    raise

                keycode = data.split('\x00')[0]

                if keycode != 'ERR':
                    try:
                        values = [self.load_arg(json.loads(val)) for val in data.split('\x00')[1:]]

                    except json.JSONDecodeError:
                        print(data.replace('\x00', ' \x1B[1m|\x1B[0m '))
                        raise

                if keycode == 'EVENT':
                    self.manager.emit(self.players[values[0]], tuple(values[1]) if isinstance(values[1], list) else values[1], *values[2:])

                elif keycode == 'INIT_LEVELS':
                    nl = dict(self.manager.levels)

                    for lid, lvl in self.manager.levels.items():
                        if lvl is not self.manager.default_level:
                            del nl[lid]

                    self.manager.levels = nl

                    for v in values[1:]:
                        lid = v['lid']
                        deltas = v['deltas']

                        self.manager.add_level_save(lid, v)

                    self.manager.change_level(values[0])

                    print('Received levels.')

                elif keycode == 'INIT_ENTITIES':
                    for v in values:
                        eid = v['eid']
                        level = v.get('level', None)
                        components = v['components']

                    if level:
                        e = self.manager.levels[level].create_entity(components, eid)

                    else:
                        e = self.manager.levels[level].create_entity(components, eid)

                    if e.has('name', 'player'):
                        self.players[e['name'].value] = e

                    print('Received entities.')

                elif keycode == 'ERR':
                    raise RuntimeError(repr(data))

        if player:
            self._write('\x00'.join(
                ['JOIN', *[json.dumps(dump_arg(arg)) for arg in [
                    player['name'].value, player.id, *[
                        [comp.name, comp.value, type(comp).__name__] for comp in player.get_components()
                    ]
                ]]]
            ).encode('utf-8') + b'\n')

            while self.events:
                e = self.events.pop(0)
                self.send_event(e)
            
            self.events = None

        while True:
            sleep_amount = 1 / 30

            try:
                data = self.client.recv(4096)

                if data == b'':
                    self.stop()
                    return

                else:
                    await _recv(data)

            except ConnectionResetError:
                self.stop()
                return

            except BlockingIOError:
                sleep_amount = 1 / 20

            sent = self.client.send(self.outbound)
            self.outbound = self.outbound[sent:]

            if self.outbound:
                sleep_amount = 0
            
            await trio.sleep(sleep_amount)
        

class Server(object):
    def load_arg(self, arg):
        if arg['type'] == 'vec':
            return Vector(arg['coord'])

        elif arg['type'] == 'normal':
            return arg['value']

        elif arg['type'] == 'component':
            c = self.manager.find_entity(arg['eid'])[arg['name']]
            c.force_set(arg['value'])
            return c

        elif arg['type'] == 'entity':
            return self.manager.find_entity(arg['eid'])

        elif arg['type'] == 'window':
            return self.manager.window
        
        else:
            raise ValueError("Unknown JSON argument type: {}".format(repr(arg['type'])))

    def __init__(self, manager: Manager, port: int, player_type: str = 'player'):
        self.manager = manager
        self.player_names = set()
        self.clients = {}
        self.players = {}
        self.outbound = {}
        self.port = int(port)
        self.player_type = player_type
        self.running = False

        @self.manager.global_listener
        def broadcast_event(source, name, *args, **kwargs):
            for s, c in self.clients.items():
                player = self.players[s] 

                if player and source.has('player', 'name') and (not player or source is not player):
                    self._write(s, '\x00'.join(['EVENT', *(json.dumps(dump_arg(a)) for a in [source['name'].value, name, *args])]).encode('utf-8') + b'\n')

        self.buffer = ''

    def _write(self, s, data):
        self.outbound[s] += data

    async def accept(self, client, address):
        session = str(uuid.uuid4())
        self.outbound[session] = b''

        self.players[session] = None
        self.clients[session] = None

        commands = {}

        def _write(data):
            self._write(session, data)

        async def _recv(data):
            try:
                lines = (_recv.buffer + data.decode('utf-8')).split('\n')

            except ValueError:
                _write(b'ERR\x00102\x00malformed command line buffering' + b'\n')

            _recv.buffer = lines[-1]

            for command in lines[:-1]:
                command = command.strip()

                try:
                    name = command.split('\x00')[0]

                except ValueError:
                    _write(b'ERR\x00103\x00malformed command arguments' + b'\n')

                for target_name, func in commands.items():
                    if name.upper() == target_name.upper():
                        #print('  -  Executing command:', target_name.upper())
                        values = []

                        for val in command.split('\x00')[1:]:
                            try:
                                values.append(self.load_arg(json.loads(val)))

                            except json.JSONDecodeError:
                                _write(b'ERR\x00101\x00bad JSON data' + b'\n')
                                print(command.replace('\x00', ' \x1B[1m|\x1B[0m '))
                                return

                            except BaseException as err:
                                print(command.replace('\x00', ' \x1B[1m|\x1B[0m '))
                                raise
                        
                        func(*values)

        _recv.buffer = ''


        def command(target_name: str):
            def _decorator(func: Callable):
                commands[target_name] = func
                return func
                                
            return _decorator

        @command('join')
        def on_join(name, eid, *components):
            if self.players[session]:
                print('/!\ Already joined:', name)
                _write(b'ERR\x00201\x00already joined' + b'\n')

            elif name in self.player_names:
                print('/!\ Name taken:', name)
                _write(b'ERR\x00203\x00name taken' + b'\n')

            else:
                print('Joined:', name, '(id: {})'.format(eid))

                self.players[session] = self.manager.create_templated_entity(self.player_type, [('name', name), *(c for c in components if c[0] != 'localplayer')], eid)

                if 'localplayer' in self.players[session]:
                    del self.players[session]['localplayer']

                lvls = []

                for lid, level in self.manager.levels.items():
                    lvls.append({
                        'lid': lid,
                        'deltas': level.deltas
                    })

                _write('\x00'.join(['INIT_LEVELS', *(json.dumps(dump_arg(x)) for x in [self.manager.current_level.id, *lvls])]).encode('utf-8') + b'\n')

                loaded = []

                for entity in self.manager:
                    comp = [(comp.name, comp.value, type(comp).__name__) for comp in entity.get_components() if comp.name != 'localplayer']

                    if entity is self.players[session]:
                        comp.append(('localplayer',))

                    e = {
                        'eid': entity.id,
                        'components': comp
                    }

                    if entity.level is not self.manager:
                        e['level'] = entity.level.id

                    loaded.append(e)

                _write('\x00'.join(['INIT_ENTITIES', *(json.dumps(dump_arg(x)) for x in loaded)]).encode('utf-8') + b'\n')

        @command('leave')
        def on_leave():
            if self.players[session] is None:
                _write(b'ERR\x00202\x00not in the game' + b'\n')
                print('/!\ Not in the game', address)

            else:
                print('Left:', self.players[session]['name'].value)
                self.players[session].remove()

        @command('event')
        def on_event(event_name, *args):
            self.manager.emit(self.players[session], event_name, *args)

        while True:
            sleep_amount = 1 / 30

            try:
                data = client.recv(4096)

                if data == b'':
                    self.stop()
                    return

                else:
                    await _recv(data)

            except ConnectionResetError:
                self.stop()
                return

            except BlockingIOError:
                sleep_amount = 1 / 20

            sent = client.send(self.outbound[session])
            self.outbound[session] = self.outbound[session][sent:]

            if self.outbound:
                sleep_amount = 0
            
            await trio.sleep(sleep_amount)
        
    async def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)

        self.running = True

        async with trio.open_nursery() as nursery:
            while self.running:
                try:
                    (conn, addr) = self.socket.accept()

                except BlockingIOError:
                    await trio.sleep(0.3)

                else:
                    nursery.start_soon(self.accept, conn, addr)
                    await trio.sleep(0.2)

    def stop(self):
        self.running = False