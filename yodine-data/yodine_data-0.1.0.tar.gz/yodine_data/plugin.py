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

from pyglet.window import key
from .inventory import ItemContainer



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
                return None

            if 'bounding_box' not in ent:
                ent['bounding_box'] = [30, 30]

            vec = ComponentVector(ent['position'])
            box = ComponentVector(ent['bounding_box'])

            #print(box, (
            #    abs(vec.x - x * 35 - 35 / 2),
            #    abs(vec.y - y * 35 - 35 / 2)
            #))

            dx = abs(vec.x - x * 35 - 35 / 2)
            dy = abs(vec.y - y * 35 - 35 / 2)

            collision = (
                dx <= box.x / 2 + 35 / 2 and
                dy <= box.y / 2 + 35 / 2
            )

            if collision:
                if dx > dy:
                    return "horizontal"

                else:
                    return "vertical"

            return None

        def on_move(self, manager, entity, start_pos):
            for ((x, y), tt) in manager.current_level.tiles.items():
                if tt == self.name:
                    col = self.collides(manager, entity, x, y)

                    if col:
                        if col == 'horizontal':
                            ComponentVector(entity['position']).x = start_pos.x

                        else:
                            ComponentVector(entity['position']).y = start_pos.y

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
        player = game.manager.current_level.create_templated_entity('player')
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

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, position, velocity):
            vel = ComponentVector(velocity)

            if vel.sqsize() > 0:
                pos = ComponentVector(position)
                oldpos = Vector(pos)
                pos << pos + vel * dtime

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
            ('speed', 22),
            ('inventory', {}, 'InventoryComponent'),
            ('player',),
            ('bounding_box', (20, 20)),
        ]


    @loader.template
    class T_FPSCounter(EntityTemplate):
        name = 'fpscounter'
        group = 'overlays'

        default_components = [
            ('fpscounter',)
        ]

    player_img = pyglet.image.load(asset_path('sprites/a_shitty_wallaby.png'))
    player_img.anchor_x = int(player_img.width / 2)
    player_img.anchor_y = int(player_img.height / 2)

    @loader.system_type
    class S_PlayerRender(System):
        component_types = ['position', 'angle', 'player']

        def system_init(self):
            self.sprites = {}

        def on_spawned(self, entity: Entity, position, angle, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(player_img)

        def render(self, entity: Entity, window: pyglet.window.Window, position, angle, **kwargs):
            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite

            vec = ComponentVector(position)
            newvec = Vector(entity.manager.camera_transform(window, vec.x, vec.y))

            sprite.x, sprite.y = newvec.x, newvec.y
            sprite.rotation = math.degrees(angle.value) + 180

            sprite.draw()


    @loader.system_type
    class S_PlayerMovement(System):
        component_types = ['position', 'toward', 'velocity', 'player_move', 'speed', 'angle']

        def on_mouse_move(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, position, velocity, speed, toward, angle, **kwargs):
            angle.value = math.pi - math.atan2(
                new_pos.y - self.manager.game.window.height / 2,
                new_pos.x - self.manager.game.window.width / 2,
            )

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, position, velocity, speed, toward, angle, **kwargs):
            self.manager.set_camera(*position.value)
            speed = speed.value

            vel = ComponentVector(velocity)
            tow = ComponentVector(toward)

            if keyboard[key.UP]:
                tow.y = 1

            elif keyboard[key.DOWN]:
                tow.y = -1

            if keyboard[key.LEFT]:
                tow.x = -1

            elif keyboard[key.RIGHT]:
                tow.x = 1

            vel /= 1 + 0.4
            vel += tow.rotate(angle.value) * speed
            tow /= 2


    @loader.component_type
    class InventoryComponent(Component, ItemContainer):
        def __init__(self, *args, **kwargs):
            ItemContainer.__init__(self)
            Component.__init__(self, *args, **kwargs)
            
        def get(self):
            return self.items

        def set(self, value):
            self.items = value