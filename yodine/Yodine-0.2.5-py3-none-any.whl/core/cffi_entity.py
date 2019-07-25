import pyglet
import threading
import queue

from .entity import TileType, ComponentType
from .cffi.entity import ffi, lib
from typing import Type, Iterator, Optional, Iterable, Tuple, Any, Union
from .extension import ModLoader
from .vector import Vector, ComponentVector

try:
    import simplejson as json

except ImportError:
    import json



indexes = {}

@ffi.def_extern()
def _entity_iter_callback(ei, e):
    indexes[ei]._iterated(e)


component_types = {}

def register_component(cotype):
    component_types[cotype.__name__] = cotype
    return cotype

@register_component
class Component(object):
    def __init__(self, entity: 'Entity', name: str = None, value: Optional[Any] = None, c_def = None):
        self.entity = entity

        if c_def:
            self._comp = c_def

        else:
            self._comp = lib.allocComponent(entity.c_entity._entity, name.encode('utf-8'), json.dumps(value).encode('utf-8'))
    
    def set(self, value):
        #lib.setComponent(self.entity._entity, self.name, json.dumps(value))
        self._comp.jsonValue = ffi.new('char[]', json.dumps(value).encode('utf-8'))

    def __repr__(self):
        return '[{} {} = {}]'.format(type(self).__name__, self.name, repr(self.value))

    def __getattr__(self, name):
        if name == 'value':
            return self.get()

        elif name == 'name':
            return ffi.string(self._comp.name).decode('utf-8')

        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'value':
            self.set(value)

        elif name == 'name':
            self._comp.name = name.encode('utf-8')

        else:
            super().__setattr__(name, value)

    def get(self):
        return json.loads(ffi.string(self._comp.jsonValue))


class Entity(object):
    def __init__(self, manager: 'Manager', components: Optional[Iterable[Tuple[str, Any]]] = None, identifier = None, c_def = None):
        self.manager = manager

        if c_def:
            self.c_entity = c_def

        else:
            self.c_entity = C_Entity(None, lib.allocEntity(ffi.NULL, identifier or lib.makeUUID(), ffi.NULL))

            for c in components:
                self.add_component(*c)

    def __contains__(self, name):
        return name in self.c_entity

    def __hash__(self):
        return hash(self.c_entity._entity.id)

    def remove(self):
        lib.removeEntity(self.manager.entity_index._ei, self.c_entity._entity)

    def add_component(self, name: str, value: Optional[Any] = None, st: Union[ComponentType, str] = None) -> Component:
        c = lib.setComponent(self.c_entity._entity, name.encode('utf-8'), json.dumps(value).encode('utf-8'))
        
        if isinstance(st, type) and issubclass(st, Component):
            if st is not Component:
                st = st.__name__

            else:
                st = None

        if st:
            c.specialType = ffi.new("char[]", st.encode('utf-8'))

        return Component(self, c_def=c)

    def __getitem__(self, comp_name: str) -> Component:
        res = lib.findComponent(self.c_entity._entity, comp_name.encode('utf-8'))

        if not res or res is ffi.NULL:
            raise KeyError("No such component: " + repr(comp_name))

        return Component(self, c_def=res)

    def __setitem__(self, comp_name: str, value: Optional[Any] = None):
        lib.setComponent(self.c_entity._entity, comp_name.encode('utf-8'), json.dumps(value).encode('utf-8'))


class C_Entity(object):
    def __init__(self, index: 'C_EntityIndex', _entity):
        self.index = index
        self._entity = _entity

    def __contains__(self, name):
        c = lib.findComponent(self._entity, name.encode('utf-8'))
        return c and c is not ffi.NULL

    def add_py_component(self, c: 'Component'):
        st = None
        
        if type(c) is not Component:
            st = type(c).__name__

        c = lib.setComponent(self._entity, c.name.encode('utf-8'), json.dumps(c.value).encode('utf-8'))
        
        if st:
            c.specialType = ffi.new("char[]", st.encode('utf-8'))


class Level(object):
    def __init__(self, lid: str, manager: 'Manager', width: int = 500, height: int = 500):
        self.id = lid
        self.manager = manager
        self.tiles = {}
        self.deltas = []
        self.width = width
        self.height = height
        self.entities = []

    def __iter__(self) -> Iterator['Entity']:
        return iter(self.entities)

    def entities_at(self, x: int, y: int) -> Iterator['Entity']:
        left = x * 35
        right = (x + 1) * 35

        top = y * 35
        bottom = (y + 1) * 35

        for e in self.manager:
            if 'position' in e:
                pos = ComponentVector(e['position'])

                if pos.x >= left and pos.x <= right and pos.y >= top and pos.y <= bottom:
                    yield e

                del pos

    def tiles(self, tt: TileType) -> Iterator[Vector]:
        x = 0
        y = 0

        for i, tile in enumerate(self.tiles):
            if tile == tt.name:
                yield Vector((x, y))
            
            x += 1

            if x > manager.current_level.width:
                y += 1
                x = 0

    def add_entity(self, e: 'Entity') -> 'Entity':
        self.entities.append(e)
        return e

    def create_entity(self, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = Entity(self.manager, components, identifier)
        self.add_entity(e)
        
        return e

    def transform_position(self, vec: Vector) -> Vector:
        return type(vec)(int(vec.x / 35), int(vec.y / 35))

    def rectangle(self, start: Vector, width: int, height: int, tile: str):
        for y in range(int(start.y), int(start.y) + height):
            for x in range(int(start.x), int(start.x) + width):
                self.tiles[x, y] = tile

        self.deltas.append(('rect', int(start.x), int(start.y), width, height, tile))

    def set(self, pos: Vector, tile: str):
        self.tiles[int(pos.x), int(pos.y)] = tile
        self.deltas.append(('set', int(pos.x), int(pos.y), tile))

    def save(self):
        return json.dumps({ 'width': self.width, 'height': self.height, 'deltas': self.deltas})

    def load(self, data: str):
        self.load_save(json.loads(data))

    def load_save(self, save):
        self.width = save['width']
        self.height = save['height']
        self.deltas = []
        deltas = save['deltas']

        self.tiles = {}

        for d in self.deltas:
            kind = d[0]

            if kind == 'set':
                self.set(Vector(d[1], d[2]), *d[3:])

            elif kind == 'rect':
                self.rectangle(Vector(d[1], d[2]), *d[3:])

            else:
                raise ValueError("Unknown level delta type: " + repr(kind))

    def render(self, window: pyglet.window.Window):
        for (x, y), tile in self.tiles.items():
            if tile:
                t = self.manager.tile_types[tile]
                t.render(window, self, x, y)


class Manager(object):
    def __init__(self, game, entities = None):
        self.game = game # type; yodine.game.Game
        self.entity_index = C_EntityIndex()
        self.systems = [] # type: List[System]
        self.event_listeners = {} # type: Dict[str, Callable]
        self.templates = {}
        self.tile_types = {} # type: Dict[str, TileType]
        self.component_types = component_types
        self.camera = Vector((0, 0))
        self.current_level = None # type: Level
        self.levels = {} # type: Dict[str, Level]
        self.loader = ModLoader()

    def __len__(self):
        return len(self.entity_index)

    def change_level(self, lid: str):
        moving = bool(self.current_level)
        self.current_level = self.levels[lid]
        
        if moving:
            carry = []

            for e in self:
                if 'carry' in e:
                    carry.append(e)

            del self.entity_index
            self.entity_index = C_EntityIndex()

            for c in carry:
                self.add_entity(c)

        for e in self.current_level.entities:
            self.add_entity(e)

    def add_level_save(self, lid: str, save) -> 'Level':
        l = Level(lid, self, save['width'], save['height'])
        l.load_save(save)

        return self.add_level(l)

    def add_level(self, level: 'Level') -> 'Level':
        self.levels[level.id] = level
        return level

    def create_level(self, lid: str, width: int, height: int) -> 'Level':
        return self.add_level(Level(lid, self, width, height))

    def add_tile_type(self, tt: 'TileType'):
        self.tile_types[tt.name] = tt

    def move_camera(self, x, y):
        self.camera += Vector((x, y))

    def set_camera(self, x, y):
        self.camera.x = x
        self.camera.y = y

    def load_mod(self, plugin_name: str):
        self.loader.load_one(plugin_name)
        self.loader.apply(self)

    def load_all_mods(self):
        self.loader.load_all()
        self.loader.apply(self)

    def register_template(self, template: Type['EntityTemplate']) -> Type['EntityTemplate']:
        self.templates[template.name] = template(self)
        return template

    def register_component(self, cotype: Type['Component']) -> Type['Component']:
        self.component_types[cotype.__name__] = cotype
        return cotype

    def __iter__(self) -> Iterator['Entity']:
        return (Entity(self, c_def=_e) for _e in iter(self.entity_index))

    def tick(self, *args):
        def _on_iter(e):
            for s in self.systems:
                s._tick(e, *args)

        for t in self.tile_types.values():
            t.tick(self, *args)

    def render(self, window: pyglet.window.Window):
        window.clear()

        if self.current_level:
            self.current_level.render(window)

        def _on_iter(e):
            for s in self.systems:
                s._render(e, window)

        self.iterate(_on_iter)

    def iterate(self, callback):
        def _on_iter(e):
            callback(Entity(self, c_def=e))

        self.entity_index.iterate(_on_iter)

    def apply(self, window: pyglet.window.Window) -> pyglet.window.Window:
        @window.event
        def on_draw():
            self.render(window)

        return window

    def add_system(self, s: Type['System']) -> None:
        self.systems.append(s(self))

    def remove_entity(self, e: 'Entity') -> None:
        del self.entity_index[e.id]

    def create_entity(self, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        #e = Entity(self, components, identifier)
        #self.add_entity(e)
        e = Entity(self, c_def=self.entity_index.create_entity(components, identifier))
        self.emit(e, 'spawn')
        
        return e

    def iter_grouped_templates(self, template_group: str) -> Iterator[Type['EntityTemplate']]:
        for template in self.templates:
            a = template.group.split('.')
            b = template_group.split('.')

            a = a[:len(b)]

            if tuple(a) == tuple(b):
                yield template

    def create_templated_entity(self, template_name: str, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.templates[template_name]
        ent = e.spawn(components, identifier)
        return self.add_entity(ent)

    def add_entity(self, e: 'Entity') -> None:
        self.entity_index.add_entity(e.c_entity)

    def listen(self, event_name):       
        def _decorator(self, func):
            if event_name not in self.event_listeners:
                self.event_listeners[event_name] = set()
            
            self.event_listeners[event_name] |= {func}
            return func

        return _decorator

    def add_listener(self, event_name, func):
        if event_name not in self.event_listeners:
            self.event_listeners[event_name] = set()

        self.event_listeners[event_name] |= {func}

    def emit(self, source, event_name, *args, **kwargs):
        if event_name in self.event_listeners:
            for func in self.event_listeners[event_name]:
                func(source, *args, **kwargs)

        check_name = '_'.join(event_name) if isinstance(event_name, (tuple, list)) else event_name

        for system in self.systems:
            system._on(check_name, source, *args, **kwargs)

        for tt in self.tile_types.values():
            tt._on(self, check_name, source, *args, **kwargs)

    def emit_all(self, event_name, *args, **kwargs):
        for e in self:
            self.emit(e, event_name, *args, **kwargs)

    def __getitem__(self, entity_id: str) -> 'Entity':
        return self.entity_index.get(entity_id, None)


class C_EntityIndex(object):
    def __init__(self):
        self._ei = lib.allocIndex()
        indexes[self._ei] = self
        self._iter_stack = []

    def __len__(self):
        return lib.indexSize(self._ei)

    def create_entity(self, components, uuid = None):
        e = self._wrap_entity(lib.allocEntity(self._ei, uuid or lib.makeUUID(), ffi.NULL))

        for c in components:
            e.create_component(*c)

        return e

    def add_entity(self, entity: C_Entity):
        lib.addEntity(self._ei, entity._entity)

    def __del__(self):
        lib.deallocIndex(self._ei)

    def iterate(self, callback):
        self._iter_stack.append(callback)
        lib.iterEntities(self._ei)

        self._iter_stack.pop()

    def _wrap_entity(self, e):
        return C_Entity(self, e)

    def _iterated(self, e):
        if len(self._iter_stack) > 0:
            self._iter_stack[0](self._wrap_entity(e))

        else:
            raise RuntimeError("Attempted to iterate on C_EntityIndex entities, but no callback was defined!")

    def __iter__(self):
        q = queue.Queue()
        job_done = object()

        def _iter_callback(e):
            q.put_nowait(e)

        def _iterate(c):
            self.iterate(c)
            q.put_nowait(job_done)

        t = threading.Thread(target=_iterate, args=(_iter_callback,))
        t.start()
        
        while True:
            e = q.get(True, 1 / 50)

            if e is job_done:
                break

            yield e

    def get(self, uuid, default = None):
        res = self._wrap_entity(lib.findEntity(self._ei, uuid))

        if res is ffi.NULL:
            return default

        return res


if __name__ == '__main__':
    mg = Manager(None)
    mg.create_entity()