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
from yodine.core.entity import EntityTemplate, Entity, System, TileType
from yodine.core.extension import ModLoader
from yodine.core.vector import ComponentVector, Vector
from yodine.game import Game

# Other imports go below.
import os
import pyglet



# These helper functions will access assets for you :)
def asset_path(asset_name: str) -> str:
    return os.path.join(os.path.split(__file__)[0], 'data', asset_name)


def open_asset(asset_name: str):
    return open(asset_path(asset_name))


# This function will be called when the plugin is
# loaded.
def loaded(loader: ModLoader):
    # === Routines ===

    def get_pos(entity: Entity, component_name: str = 'position') -> ComponentVector:
        assert component_name in entity
        return ComponentVector(*entity[component_name])

    # Defines a standard tile type (background - does nothing).
    class FloorTileType(TileType):
        name = 'floor'

    loader.add_tile_type(FloorTileType(pyglet.resource.image(asset_path('tiles/floor.png'))))

    # Defines a custom tile type (foreground - e.g. collides).
    class WallTileType(TileType):
        name = 'wall'

        def on_move(self, manager, entity, start_pos):
            if self.is_inside(manager, entity):
                ComponentVector(entity['position']) << start_pos

    loader.add_tile_type(WallTileType(pyglet.resource.image(asset_path('tiles/wall.png'))))

    # Defines a routine, which may be used by this or other
    # plugins.
    @loader.routine()
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

        start_level = manag.create_level('start', 30, 30)
        start_level.rectangle(Vector((-20, -20)), 20, 20, 'floor')

        start_level.rectangle(Vector((-21, -21)), 1, 20, 'wall')
        start_level.rectangle(Vector((21, -21)), 1, 20, 'wall')

        start_level.rectangle(Vector((-20, -21)), 20, 1, 'wall')
        start_level.rectangle(Vector((-20, -21)), 20, 1, 'wall')

        manag.change_level(start_level)

        return start_level

    @loader.routine('init.yodine')
    def init_player(game: Game):
        return game.manager.create_templated_entity('player')

    # === Systems ===

    # Defines a system to be registered by
    # the loader.

    @loader.system_type
    class LabelRenderSystem(System):
        commponent_types = ['name', 'position']

        def render(self, entity: Entity, window: pyglet.window.Window, name, position, *args, **kwargs) -> None:
            pos = get_pos(entity)

            label = pyglet.text.Label(
                name,
                anchor_x = 'center',
                anchor_y = 'center',
                x = pos.x - self.manager.camera.x,
                y = pos.y + 90 - self.manager.camera.y,
                bold = True
            )

    @loader.system_type
    class MovementSystem(System):
        pass

    # Defines an entity template, a way to specify how certian
    # entities should be created.
    @loader.template
    class MyPluginEntityType(EntityTemplate):
        # The name of this template. Used when looking it up.
        name = 'Cow'

        # The group of this template. Used when looking a specific group of templates up.
        group = 'living.passive'

        # A list of default components.
        default_components = [
            ('name', 'a cow'),
            ('postfix', 'MOOO!'),
            ('moo', 'YES!')
        ]


