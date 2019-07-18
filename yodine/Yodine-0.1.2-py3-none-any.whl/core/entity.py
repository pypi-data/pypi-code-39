import sqlite3
import uuid
import collections
import traceback
import warnings
import math
import json
import pyglet
import typing
import itertools

from typing import Optional, Iterable, Any, Tuple, TypeVar, Type, Iterator, Union, Callable
from .extension import ModLoader
from .vector import Vector, ComponentVector
from pyglet import gl



ComponentType = Type['Component']


class EntityContainer(object):
    def __init__(self):
        self.entity_component_index = {} # dict[entity => dict[component name => A implements Component]]
        self.entity_ids = [] # list<entity id>
        self.entity_id_set = set() # set<entity id>
        self.entity_count = 0

    def get_entities(self):
        return EntityContainer.__iter__(self)

    def get_component_types(self):
        return self.component_types

    def __len__(self):
        return self.entity_count

    def __iter__(self) -> Iterator['Entity']:
        return (Entity(self, eid) for eid in self.entity_ids)

    def create_entity(self, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        if not identifier:
            identifier = str(uuid.uuid4())
            
        e = Entity(self, identifier)

        for c in components:
            e.create_component(*c)

        getattr(self, 'manager', self).emit_all('spawn', e)
        getattr(self, 'manager', self).emit(e, 'spawned')

        return e

    def create_templated_entity(self, template_name: str, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.templates[template_name]
        ent = e.spawn(self, components, identifier)
        
        return ent

    def remove_entity(self, e: 'Entity') -> None:
        if e.level is self:
            e.remove()


# === Level data ===

class TileType(object):
    name = None # type: str

    def __init__(self, sprite: pyglet.resource.image):
        self.image = sprite.get_texture()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)   

        size = 35

        self.image.width = size
        self.image.height = size

        self.sprite_cache = {}

    def unset(self, level: 'Level', x, y):
        if (x, y) in self.sprite_cache:
            self.sprite_cache[x, y].delete()
            del self.sprite_cache[x, y]

    def force_render_tile(self, window: pyglet.window.Window, level: 'Level', wx, wy):
        pyglet.sprite.Sprite(self.image, wx, wy).draw()

    def render(self, window: pyglet.window.Window, level: 'Level', x, y, wx, wy):
        #self.sprite.blit(wx, wy)
        if (x, y) in self.sprite_cache:
            sprite = self.sprite_cache[x, y]
            sprite.position = (wx, wy)

        else:
            self.sprite_cache[x, y] = pyglet.sprite.Sprite(self.image, wx, wy, batch=level.batch)

    def tick(self, manager: 'Manager', *args):
        pass

    def is_inside(self, manager: 'Manager', ent: 'Entity') -> bool:
        if 'position' not in ent:
            return False

        vec = ComponentVector(ent['position'])
        x = math.floor(vec.x / 35)
        y = math.floor(vec.y / 35)
        
        return manager.current_level.tiles.get((x, y), None) == self.name
        
    def _on(self, manager, event_name: str, entity: 'Entity', *args, **kwargs):
        if hasattr(self, 'on_' + event_name):
            return getattr(self, 'on_' + event_name)(manager, entity, *args, **kwargs)

class Trigger(object):
    def __init__(self, level: EntityContainer, x, y, width = 1, height = 1):
        self.level = level
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.inside = set()

    def is_inside(self, ent: 'Entity') -> bool:
        if 'position' not in ent:
            return False

        left = self.x * 35
        right = (self.x + self.width) * 35
        top = self.y * 35
        bottom = (self.y + self.height) * 35

        vec = ComponentVector(ent['position'])
        
        return vec.x >= left and vec.x <= right and vec.y >= top and vec.y <= bottom

    def tick(self, *args):
        for e in self.level.manager:
            if self.is_inside(e):
                if e not in self.inside:
                    self.inside.add(e)
                    self.triggered(e)

            elif e in self.inside:
                self.inside.remove(e)
    


# === Entity Component System ===



class Level(EntityContainer):
    def __init__(self, lid  : str, manager: 'Manager'):
        EntityContainer.__init__(self)
    
        self.id = lid
        self.manager = manager
        self.tiles = {}
        self.deltas = []
        self.batch = pyglet.graphics.Batch()

    def __iter__(self) -> Iterator['Entity']:
        for e in self.get_entities():
            yield e

        for e in self.manager.get_entities():
            yield e

    def emit(self, source, event_name, *args):
        return self.manager.emit(source, event_name, *args)

    def create_templated_entity(self, template_name: str, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> 'Entity':
        e = self.manager.templates[template_name]
        ent = e.spawn(self, components, identifier)
        
        return ent

    def get_component_types(self):
        return self.manager.get_component_types()

    def entities_at(self, x: int, y: int) -> Iterator['Entity']:
        left = x * 35
        right = (x + 1) * 35

        top = y * 35
        bottom = (y + 1) * 35

        for e in self.get_entities():
            if 'position' in e:
                pos = ComponentVector(e['position'])

                if pos.x >= left and pos.x <= right and pos.y >= top and pos.y <= bottom:
                    yield e

                del pos

    def tiles(self, tt: TileType) -> Iterator[Vector]:
        for xy, tile in self.tiles.items():
            if tile == tt.name:
                yield Vector(xy)

    def transform_position(self, vec: Vector) -> Vector:
        return type(vec)(int(vec.x / 35), int(vec.y / 35))

    def rectangle(self, start: Vector, width: int, height: int, tile: str):
        for y in range(int(start.y), int(start.y) + height):
            for x in range(int(start.x), int(start.x) + width):
                if (x, y) in self.tiles:
                    self.manager.tile_types[self.tiles[x, y]].unset(self, x, y)

                self.tiles[x, y] = tile

        self.deltas.append(('rect', int(start.x), int(start.y), width, height, tile))

    def set(self, pos: Vector, tile: str):
        if (int(pos.x), int(pos.y)) in self.tiles:
            self.manager.tile_types[self.tiles[int(pos.x), int(pos.y)]].unset(self, int(pos.x), int(pos.y))

        self.tiles[int(pos.x), int(pos.y)] = tile
        self.deltas.append(('set', int(pos.x), int(pos.y), tile))

    def save(self):
        return json.dumps({ 'deltas': self.deltas})

    def load(self, data: str):
        self.load_save(json.loads(data))

    def load_save(self, save):
        self.deltas = []
        deltas = save['deltas']

        self.tiles = {}

        for d in self.deltas:
            self.apply_delta(d)

    def apply_delta(self, d):
        kind = d[0]
        self.deltas.append(d)

        if kind == 'set':
            self.set(Vector((d[1], d[2])), *d[3:])

        elif kind == 'rect':
            self.rectangle(Vector((d[1], d[2])), *d[3:])

        else:
            raise ValueError("Unknown level delta type: " + repr(kind))

    def render(self, window: pyglet.window.Window):
        for (x, y), tile in self.tiles.items():
            if tile:
                wx = x * 35 - self.manager.camera.x + window.width / 2
                wy = y * 35 - self.manager.camera.y + window.height / 2

                if wx > -35 and wx < window.width + 35 and wy > -35 and wy < window.height + 35:
                    t = self.manager.tile_types[tile]
                    t.render(window, self, x, y, wx, wy)

        self.batch.draw()

class Manager(EntityContainer):
    def __init__(self, game):
        EntityContainer.__init__(self)

        self.game = game # type; yodine.game.Game
        #self.entity_list = []
        #self.entity_index = {}

        self.systems = [] # type: List[System]
        self.event_listeners = {} # type: Dict[str, Callable]
        self.templates = {}
        self.tile_types = {} # type: Dict[str, TileType]
        self.component_types = component_types
        self.camera = Vector((0, 0))
        self.levels = {} # type: Dict[str, Level]
        self.default_level = self.create_level('_DEFAULT')
        self.current_level = self.default_level # type: Level
        self.loader = ModLoader()

    def camera_transform(self, window, x, y):
        return (x - self.camera.x + window.width / 2, y - self.camera.y + window.height / 2)

    def force_render_tile(self, window: pyglet.window.Window, tiletype: str, wx, wy):
        self.tile_types[tiletype].force_render_tile(self.current_level, window, wx, wy)

    def un_camera_transform(self, window, x, y):
        return (x + self.camera.x - window.width / 2, y + self.camera.y - window.height / 2)

    def __iter__(self) -> Iterator['Entity']:
        for e in self.get_entities():
            yield e

        if self.current_level is not None:
            for e in self.current_level.get_entities():
                yield e

    def change_level(self, lid: str):
        self.current_level = self.levels[lid]

    def add_level_save(self, lid: str, save) -> Level:
        l = Level(lid, self, save['width'], save['height'])
        l.load_save(save)

        return self.add_level(l)

    def add_level(self, level: Level) -> Level:
        self.levels[level.id] = level
        return level

    def create_level(self, lid: str) -> Level:
        return self.add_level(Level(lid, self))

    def add_tile_type(self, tt: TileType):
        self.tile_types[tt.name] = tt

    def move_camera(self, x, y):
        self.camera += Vector((x, y))

    def set_camera(self, x, y):
        self.camera.x = x
        self.camera.y = y

    def load_mod(self, plugin_name: str):
        self.loader.load_one(plugin_name)

        for r in self.loader.routines['preload.' + plugin_name]:
            r(self.game)

        self.loader.apply(self)

        for r in self.loader.routines['postload.' + plugin_name]:
            r(self.game)

    def apply_mod(self, plugin_name: str, func: Callable):
        self.loader.load(plugin_name, func)

        for r in self.loader.routines['preload.' + plugin_name]:
            r(self.game)

        self.loader.apply(self)

        for r in self.loader.routines['postload.' + plugin_name]:
            r(self.game)

    def load_all_mods(self):
        for plugin_name in self.loader.load_all():
            for r in self.loader.routines['preload.' + plugin_name]:
                r(self.game)

            self.loader.apply(self)

            for r in self.loader.routines['postload.' + plugin_name]:
                r(self.game)

    def register_template(self, template: Type['EntityTemplate']) -> Type['EntityTemplate']:
        self.templates[template.name] = template(self)
        return template

    def register_component(self, cotype: Type['Component']) -> Type['Component']:
        self.component_types[cotype.__name__] = cotype
        return cotype

    def tick(self, *args):
        for e in self:
            for s in self.systems:
                s._tick(e, *args)

        for t in self.tile_types.values():
            t.tick(self, *args)

    def render(self, window: pyglet.window.Window):
        window.clear()

        if self.current_level is not None:
            self.current_level.render(window)

        for e in self:
            for s in self.systems:
                s._render(e, window)

    def apply(self, window: pyglet.window.Window) -> pyglet.window.Window:
        @window.event
        def on_draw():
            self.render(window)

        return window

    def reset_systems(self):
        self.systems = []

    def add_system(self, s: Type['System']) -> None:
        self.systems.append(s(self))

    def iter_grouped_templates(self, template_group: str) -> Iterator[Type['EntityTemplate']]:
        for template in self.templates:
            a = template.group.split('.')
            b = template_group.split('.')

            a = a[:len(b)]

            if tuple(a) == tuple(b):
                yield template

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


component_types = {}

def register_component(cotype):
    component_types[cotype.__name__] = cotype
    return cotype


@register_component
class Component(object):
    def __init__(self, entity: 'Entity', name: str, value: Optional[Any] = None):
        self.entity = entity
        self.name = name
        self._value = value
    
    def set(self, value):
        self._value = value
        self.entity.manager.emit(self.entity, ('change', self.name), self)

    def __repr__(self):
        return '[{} {} = {}]'.format(type(self).__name__, self.name, repr(self.value))

    def __getattr__(self, name):
        if name == 'value':
            return self.get()

        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'value':
            self.set(value)

        else:
            super().__setattr__(name, value)

    def get(self):
        return self._value


class Entity(object):
    def __init__(self, level: 'Level', identifier = None):
        self.level = level
        self.manager = getattr(level, 'manager', level)
        self.id = identifier or str(uuid.uuid4())

        self.level.entity_component_index.setdefault(self.id, {})

        if self.id not in self.level.entity_id_set:
            self.level.entity_ids.append(self.id)
            self.level.entity_id_set.add(self.id)
            self.level.entity_count += 1

    def get_components(self) -> Iterator['Component']:
        return self.level.entity_component_index[self.id].values()

    def __hash__(self):
        return hash(self.id)

    def remove(self):
        del self.level.entity_component_index[self.id]
        self.level.entity_id_set.remove(self.id)
        self.level.entity_ids.remove(self.id)
        self.level.entity_count -= 1

    def create_component(self, name: str, value = None, kind = None) -> 'Component':
        ct = self.level.get_component_types()

        if kind is None:
            kind = Component

        elif kind in ct:
            kind = ct[kind]

        elif isinstance(kind, str):
            raise ValueError("Unknown component type: " + repr(kind))

        elif not (isinstance(kind, type) and issubclass(kind, Component)):
            raise TypeError("Bad component type (expected str, Type[Component], None): " + repr(kind))

        comp = kind(self, name, value)
        self.level.entity_component_index[self.id][name] = comp

        return comp

    def __iter__(self):
        return iter(self.get_components())

    def __getitem__(self, comp_name: str) -> 'Component':
        return self.level.entity_component_index[self.id][comp_name]

    def __setitem__(self, comp_name: str, value: Optional[Any] = None):
        if comp_name in self:
            c = self[comp_name]
            c.value = value

        else:
            self.create_component(comp_name, value)

    def __contains__(self, comp_name: str) -> bool:
        return comp_name in self.level.entity_component_index[self.id]

    def __delitem__(self, comp_name: str):
        if comp_name not in self:
            return

        del self.level.entity_component_index[self.id][comp_name]

    def has(self, *comp_names: Iterable[str]) -> bool:
        return all(cn in self for cn in comp_names)

    def has_any(self, *comp_names: Iterable[str]) -> bool:
        return any(cn in self for cn in comp_names)

    def __repr__(self):
        return '<[ {} {} ]>'.format(self.id, ', '.join(repr(c) for c in self.get_components()))


class System(object):
    listeners = []
    component_types = []
    component_checks = {}
    component_defaults = {}

    def component_check(self, func):
        def _inner(source: Entity, *args, **kwargs):
            if not self.component_types:
                return func(source, *args, **kwargs)

            else:
                components = {}

                for cotype, cocheck in self.component_checks.items():
                    if cotype not in source or source[cotype].value != cocheck:
                        return

                for cotype in self.component_types:
                    if cotype in source:
                        components[cotype] = source[cotype]

                    else:
                        return

                for cotype, codefault in self.component_defaults.items():
                    if cotype not in source:
                        source[cotype] = codefault

                    components[cotype] = source[cotype]

                return func(source, *args, **components, **kwargs)

        return _inner

    def __init__(self, manager: Manager):
        self.manager = manager
        
        self.listeners = type(self).listeners
        self.component_types = type(self).component_types
        self.component_checks = type(self).component_checks
        self.component_defaults = type(self).component_defaults

        for event_name, func in self.listeners:
            manager.init_event(event_name)
            manager.add_listener(event_name, func)

        self.system_init()

    def system_init(self):
        pass
    
    def _tick(self, entity: Entity, *args) -> None:
        self.component_check(self.tick)(entity, *args)

    def _render(self, entity: Entity, window: pyglet.window.Window, *args) -> None:
        self.component_check(self.render)(entity, window, *args)

    def _on(self, event_name: str, entity: Entity, *args, **kwargs):
        if hasattr(self, 'on_' + event_name):
            return self.component_check(getattr(self, 'on_' + event_name))(entity, *args, **kwargs)

    def tick(self, entity: Entity, *args, **kwargs) -> None:
        pass

    def render(self, entity: Entity, window: pyglet.window.Window, *args, **kwargs) -> None:
        pass


class SystemRegistry(object):
    def __init__(self):
        self.system_types = []

    def define(self, sys: Type[System]) -> Type[System]:
        self.system_types.append(sys)

        return sys

    def apply(self, manager: Manager) -> None:
        for st in self.system_types:
            manager.add_system(st)


class EntityTemplate(object):
    name = None # type: str
    group = None # type: Optional[str]
    default_components = [] # type: Iterable[Tuple[str, Any]]

    def __init__(self, manager: Manager):
        self.manager = manager

    def spawn(self, level: Level, components: Optional[Iterable[Tuple[str, Any]]] = (), identifier: Optional[str] = None) -> Entity:
        components = list(components)
        has_components = set(c[0] for c in components)
        
        for dc in self.default_components:
            if dc[0] not in has_components:
                components.append(dc)

        return level.create_entity(components, identifier)



all_systems = SystemRegistry()
