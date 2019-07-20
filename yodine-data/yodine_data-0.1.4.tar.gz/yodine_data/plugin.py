# ============== yodine_data ==============
#             by Gustavo6046
# licensed under MIT
#
#   All the assets, entities and levels that come with Yodine (the game). Note there can be multiple games for Yodine (the engine).

# This is the main code of your plugin.
# Here you will add all of the logic that will
# be used by your plugin.

# The lines below import all of the classes you'll
# use from Yodine.
from yodine.core.entity import EntityTemplate, Entity, System, TileType, Component
from yodine.core.extension import ModLoader
from yodine.core.vector import ComponentVector, Vector
from yodine.game import Game

# Other imports go below.
import os
import pyglet
import math
import random

from pyglet.window import key
from .inventory import ItemContainer

try:
    import simplejson as json

except ImportError:
    import json



# Defines an extra resource path.
pyglet.resource.path.append(os.path.join(os.path.split(__file__)[0], 'assets'))
pyglet.resource.reindex()


# These helper functions will access assets for you :)
def asset_path(asset_name: str) -> str:
    return os.path.join(os.path.split(__file__)[0], 'assets', asset_name)


def open_asset(asset_name: str):
    return open(asset_path(asset_name))


# This function will be called when the plugin is
# loaded.
def loaded(loader: ModLoader):
    # === Routines ===

    def get_pos(entity: Entity, component_name: str = 'position') -> ComponentVector:
        assert component_name in entity
        return ComponentVector(entity[component_name])

    # Defines a standard tile type (background - does nothing).
    class FloorTileType(TileType):
        name = 'floor'

    loader.add_tile_type(FloorTileType(pyglet.resource.image('tiles/floor.png')))

    # Defines a custom tile type (foreground - e.g. collides).
    class WallTileType(TileType):
        name = 'wall'

        def collides(self, manager: 'Manager', ent: 'Entity', x, y) -> bool:
            if 'position' not in ent:
                return (None, 0, 0)

            if 'bounding_box' not in ent:
                ent['bounding_box'] = [25, 25]

            box = ComponentVector(ent['bounding_box'])
            pos = ComponentVector(ent['position'])

            dx = abs(pos.x - x * 35 - 35 / 2)
            dy = abs(pos.y - y * 35 - 35 / 2)

            collision = (
                dx <= box.x / 2 + 35 / 2 and
                dy <= box.y / 2 + 35 / 2
            )

            if collision:
                if dx > dy:
                    return "horizontal", dx, dy

                elif dy > dx:
                    return "vertical", dx, dy

            return (None, 0, 0)

        def on_move(self, manager, entity, start_pos):
            if 'position' not in entity:
                return

            p = ComponentVector(entity['position'])

            for ((x, y), tt) in manager.current_level.tiles.items():
                if tt == self.name:
                    col, dx, dy = self.collides(manager, entity, x, y)

                    if col:
                        if col == 'horizontal':
                            p.x = start_pos.x

                        else:
                            p.y = start_pos.y

                        if 'velocity' in entity:
                            vel = ComponentVector(entity['velocity'])

                            if col == 'horizontal':
                                vel.x *= -0.5

                            else:
                                vel.y *= -0.5

                        manager.emit(entity, 'hit_wall', col)


    loader.add_tile_type(WallTileType(pyglet.resource.image('tiles/wall.png')))

    # Defines a routine, which may be used by this or other
    # plugins.
    @loader.routine('init')
    def yodine_init(game: Game):
        # Routines can be accessed like a dict to
        # obtain all routines in a group (and its
        # subgroups), and those can also be accessed
        # via attributes directly by their name.
        for rout in loader.routines['init.yodine']:
            rout(game)

    # -> Level Definitions
    @loader.routine('init.yodine')
    def start_level(game: Game):
        manag = game.manager

        start_level = manag.create_level('start')
        start_level.rectangle(Vector((-20, -20)), 40, 40, 'floor')

        start_level.rectangle(Vector((-21, -21)), 1, 42, 'wall')
        start_level.rectangle(Vector((20, -21)), 1, 42, 'wall')

        start_level.rectangle(Vector((-20, 20)), 41, 1, 'wall')
        start_level.rectangle(Vector((-20, -21)), 41, 1, 'wall')

        manag.change_level('start')

        return start_level

    @loader.routine('init.yodine')
    def fps_counter(game: Game):
        game.manager.current_level.create_templated_entity('fpscounter')

    @loader.routine('init.yodine')
    def add_player(game: Game):
        player = game.manager.current_level.create_templated_entity('player', [
            ('localplayer',),
            ('name', os.environ.get('YODINE_NAME', 'Anon_' + str(random.randint(1, 1999)))), # party like it's 1999
        ])
        return player

    # === Systems ===

    # Defines a system to be registered by
    # the loader.

    @loader.system_type
    class S_LabelRender(System):
        component_types = ['name', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, name, position, *args, **kwargs) -> None:
            pos = get_pos(entity)

            label = pyglet.text.Label(
                name.value,
                anchor_x = 'center',
                anchor_y = 'center',
                x = pos.x - self.manager.camera.x + window.width / 2,
                y = pos.y + 90 - self.manager.camera.y + window.height / 2,
                bold = True
            )
            label.draw()


    @loader.system_type
    class S_FPSCounter(System):
        component_types = ['fpscounter']

        def render(self, entity: Entity, window: pyglet.window.Window, *args, **kwargs) -> None:
            if hasattr(self, 'dtime'):
                label = pyglet.text.Label(
                    str(round(1 / self.dtime, 1)),
                    x = 30,
                    y = 30,
                    bold = True
                )
                label.draw()

        def tick(self, entity: Entity, dtime: float, *args, **kwargs):
            self.dtime = dtime


    @loader.system_type
    class S_Velocity(System):
        component_types = ['position', 'velocity']
        component_defaults = {'friction': 0.425}

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, position, velocity, friction):
            vel = ComponentVector(velocity)

            if vel.sqsize() > 0:
                pos = ComponentVector(position)
                oldpos = Vector(pos)
                pos << pos + vel * dtime
                vel /= 1 + friction.value * dtime

                self.manager.emit(entity, 'move', oldpos)

    # Defines an entity template, a way to specify how certian
    # entities should be created.
    @loader.template
    class T_Player(EntityTemplate):
        # The name of this template. Used when looking it up.
        name = 'player'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living'

        # A list of default components.
        default_components = [
            ('name', 'a nameless player'),
            ('life', 100.0),
            ('position', [0, 0]),
            ('angle', 0),
            ('velocity', [0, 0]),
            ('player_move',),
            ('toward', [0, 0]),
            ('speed', 50),
            ('inventory', {}, 'InventoryComponent'),
            ('player',),
            ('bounding_box', (20, 20)),
            ('render', 'normal'),
            ('sprite', 'player'),
            ('pushable',),
            ('weight', 100),
            ('collides',),
        ]

    
    @loader.template
    class T_AIPlayer(EntityTemplate):
        editor_visible = True

        # The name of this template. Used when looking it up.
        name = 'bot'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living'

        # A list of default components.
        default_components = [
            ('life', 100.0),
            ('position', [0, 0]),
            ('angle', 0),
            ('velocity', [0, 0]),
            ('aiplayer',),
            ('toward', [0, 0]),
            ('speed', 50),
            ('inventory', {}, 'InventoryComponent'),
            ('player',),
            ('bounding_box', (20, 20)),
            ('render', 'normal'),
            ('sprite', 'player'),
            ('pushable',),
            ('weight', 100),
            ('collides',),
        ]


    @loader.template
    class T_Barrel(EntityTemplate):
        editor_visible = True

        # The name of this template. Used when looking it up.
        name = 'barrel'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'decoration'

        # A list of default components.
        default_components = [
            ('life', 100.0),
            ('position', [0, 0]),
            ('angle', 0),
            ('velocity', [0, 0]),
            ('inventory', {}, 'InventoryComponent'),
            ('pushable',),
            ('weight', 150),
            ('bounding_box', (38, 38)),
            ('render', 'normal'),
            ('sprite', 'barrel'),
            ('pushable',),
            ('radius', 50),
            ('collides',),
            ('friction', 0.5),
        ]



    @loader.template
    class T_FPSCounter(EntityTemplate):
        name = 'fpscounter'
        group = 'overlays'

        default_components = [
            ('fpscounter',)
        ]

    IMAGES = {}
        
    def load_sprite(name, path):
        img = pyglet.image.load(asset_path(path))
        mid = Vector((img.width / 2, img.height / 2))

        img.anchor_x = int(mid.x)
        img.anchor_y = int(mid.y)

        img.mid = mid

        IMAGES[name] = img
        return img

    @loader.routine('preload.yodine_data.sprites')
    def load_sprites(game):
        load_sprite('player', 'sprites/a_shitty_wallaby.png')
        load_sprite('barrel', 'sprites/barrel.png')
        print('Loaded sprites.')

    @loader.routine('get.yodine.sprites')
    def get_sprites():
        return IMAGES


    @loader.system_type
    class S_Collision(System):
        component_types = ['position', 'bounding_box', 'collides']

        def touches(self, entity, other_entity):
            pos1 = ComponentVector(entity['position'])
            pos2 = ComponentVector(other_entity['position'])

            box1 = ComponentVector(entity['bounding_box'])
            box2 = ComponentVector(other_entity['bounding_box'])

            wspan = box1.x + box2.x
            hspan = box1.y + box2.y

            return (
                abs(pos1.x - pos2.x) <= wspan / 2 and
                abs(pos1.y - pos2.y) <= hspan / 2
            )

        def get_weight(self, e):
            if 'weight' not in e:
                return 100

            return e['weight'].value

        def get_velocity(self, e):
            if 'velocity' not in e:
                return Vector((0, 0))

            return ComponentVector(e['velocity'])

        def on_move(self, entity, start_pos, position, **kwargs):
            p = ComponentVector(position)
            dxy = p - start_pos

            for other_entity in self.manager:
                if other_entity.id != entity.id and other_entity.has('position', 'bounding_box', 'collides') and self.touches(entity, other_entity):
                    if other_entity.has('pushable', 'velocity'):
                        w1 = self.get_weight(entity)
                        w2 = self.get_weight(other_entity)

                        v1 = self.get_velocity(entity)
                        v2 = self.get_velocity(other_entity)

                        pos2 = ComponentVector(other_entity['position'])

                        if v1.sqsize() == 0:
                            continue

                        force = w1 * v1.size()
                        energy = (pos2 - p).unit() * force / (w1 + w2)

                        new_dxy = dxy * force / (w1 + w2)
                        new_vel_1 = v1 - energy
                        new_vel_2 = v2 + energy

                        if 'velocity' in entity:
                            v1 << new_vel_1

                        else:
                            entity['position'] = start_pos + new_dxy

                        v2 << new_vel_2
                        p << start_pos

                        self.manager.emit(entity, 'push', other_entity)
                        self.manager.emit(other_entity, 'pushed', entity)

                    else:
                        p << start_pos
                        self.manager.emit(entity, 'bump', other_entity)
                        self.manager.emit(other_entity, 'bumped', entity)


    @loader.system_type
    class S_NormalRender(System):
        component_types = ['position', 'sprite']
        component_defaults = {'angle': 0}
        component_checks = {'render': 'normal'}

        def system_init(self):
            self.images = {}
            self.sprites = {}

            for r in self.manager.loader.routines['get.yodine.sprites']:
                self.images.update(r())

        def on_spawned(self, entity: Entity, position, angle, sprite, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

        def on_change_sprite(self, entity: Entity, new_sprite, **kwargs):
            if entity.id in self.sprites:
                self.sprites[entity.id].delete()
                
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])

        def render(self, entity: Entity, window: pyglet.window.Window, position, angle, **kwargs):
            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite

            vec = ComponentVector(position)
            newvec = Vector(entity.manager.camera_transform(window, vec.x, vec.y))

            sprite.x, sprite.y = newvec.x, newvec.y
            sprite.scale = self.manager.camera_zoom

            if 'localplayer' in entity:
                c_angle = -self.manager.camera_angle

            else:
                c_angle = self.manager.camera_angle

            sprite.rotation = -90 + math.degrees(angle.value + c_angle)

            if 'radius' in entity:
                rad = entity['radius'].value
                sprite.scale /= max(sprite.image.width, sprite.image.height) / rad

            if 'scale' in entity:
                scale = entity['scale'].value
                sprite.scale *= scale

            sprite.draw()


    @loader.system_type
    class S_PlayerMovement(System):
        component_types = ['position', 'toward', 'velocity', 'player_move', 'speed', 'angle', 'localplayer']

        def on_mouse_move(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, position, velocity, speed, toward, angle, **kwargs):
            ang = math.atan2(
                new_pos.y - self.manager.game.window.height / 2,
                new_pos.x - self.manager.game.window.width / 2,
            )

            if 'old_angle' in entity:
                angle.value += ang - entity['old_angle'].value

            entity['old_angle'] = ang

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, position, velocity, speed, toward, angle, **kwargs):
            vel = ComponentVector(velocity)

            self.manager.set_camera(*position.value, angle.value, 1.5 / (1 + math.sqrt(vel.size()) / 40))
            speed = speed.value

            tow = ComponentVector(toward)

            tow.x = 0
            tow.y = 0

            if keyboard[key.UP]:
                tow.x = 1

            elif keyboard[key.DOWN]:
                tow.x = -1

            if keyboard[key.LEFT]:
                tow.y = 1

            elif keyboard[key.RIGHT]:
                tow.y = -1

            vel /= 1 + 0.4

            if tow.sqsize() > 0:
                vel += tow.rotate(math.pi / 2 + angle.value).unit() * speed


    NETS = {}

    @loader.system_type
    class S_AIMovement(System):
        component_types = ['position', 'toward', 'velocity', 'speed', 'angle', 'aiplayer']
        component_defaults = { 'ai_state': 'idle', 'delta_angle': 0 }

        def hit_wall(self, entity: Entity, col: str, ai_state, toward, delta_angle, **kwargs):
            tow = ComponentVector(toward)

            if tow.sqsize() == 0:
                tow.y += random.choice([1, -1])

            delta_angle.value += tow.y

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, position, velocity, speed, toward, angle, ai_state, delta_angle, **kwargs):
            self.manager.set_camera(*position.value, angle.value)
            speed = speed.value

            vel = ComponentVector(velocity)
            tow = ComponentVector(toward)
            delta_angle.value /= 1 + 1.5 * dtime
            pos = ComponentVector(entity['position'])
            direc = Vector((
                math.cos(angle.value),
                math.sin(angle.value)
            ))

            if ai_state.value == 'idle':
                tow.x = 0

                if random.uniform(0, 1) ** dtime < 0.7:
                    delta_angle.value += random.uniform(-math.pi / 6, math.pi / 6)

                c = random.uniform(0, 1) ** dtime

                if c < 0.4:
                    ai_state.value == 'walking'

            elif ai_state.value == 'walking':
                tow.x = 0.4

                if random.uniform(0, 1) ** dtime < 0.5:
                    ai_state.value == 'idle'

            else:
                tow.x = 1

            for e in self.manager:
                if e.has('collides', 'position'):
                    pos2 = ComponentVector(e['position'])

                    if (pos2 - pos).sqsize() < (35 * 4) ** 2 and (pos2 - pos).unit().dot(direc) > 0.6:
                        tow.y += random.choice([1, -1])
                        tow.x *= 0.8 / (pos - pos2).size()
                        delta_angle.value -= tow.y * math.pi / 9

            if tow.sqsize() > 0:
                v = tow.rotate(math.pi / 2 + angle.value)

                if v.sqsize() > 1:
                    v = v.unit()

                vel += v * speed

            angle.value += delta_angle.value * dtime
            tow = 0


    @loader.component_type
    class InventoryComponent(Component, ItemContainer):
        def __init__(self, *args, **kwargs):
            ItemContainer.__init__(self)
            Component.__init__(self, *args, **kwargs)
            
        def get(self):
            return self.items

        def set(self, value):
            self.items = value