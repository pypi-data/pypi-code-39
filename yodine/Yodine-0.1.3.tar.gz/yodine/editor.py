import sys, functools
import os
import math
import pyglet
import pyglet.gl as pgl
import pyglet.window.mouse as pgmouse

from . import game
from .core.vector import Vector, ComponentVector
from .core.trig import fast_sin
from .core.entity import Entity, System, EntityTemplate
from .core.extension import ModLoader
from pyglet.window import key

try:
    import simplejson as json

except ImportError:
    import json



class Editor(game.Game):
    pass



def editor_plugin(loader: ModLoader):
    @loader.template
    class EditorCursor(EntityTemplate):
        name = 'edcursor'
        group = 'overlays'

        default_components = [
            ('position', (0, 0)),
            ('cam', (0, 0)),
            ('shown', False),
            ('age', 0),
            ('clickable', (35, 35)),
            ('position', (0, 0)),
            ('edcursor',),
            ('panspeed', 150),
        ]

    @loader.template
    class TilePaletteItem(EntityTemplate):
        name = 'edpaletteitem'
        group = 'overlays'

        default_components = [
            ('palette',),
            ('index', 0),
            ('tiletype',),
            ('clickable', (35, 35)),
            ('position', (0, 0)),
            ('selected', False),
            ('age', 0),
        ]

    
    @loader.template
    class ObjectPaletteItem(EntityTemplate):
        name = 'edobjpalette'
        group = 'overlays'

        default_components = [
            ('palette',),
            ('index', 0),
            ('template',),
            ('clickable', (35, 35)),
            ('position', (0, 0)),
            ('selected', False),
            ('age', 0),
        ]


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

        def on_spawned(self, entity: Entity, sprite, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])
            self.sprites[entity.id].rotation = -90

        def on_loaded(self, entity: Entity, sprite, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])
            self.sprites[entity.id].rotation = -90

        def on_change_sprite(self, entity: Entity, new_sprite, **kwargs):
            if entity.id in self.sprites:
                self.sprites[entity.id].delete()

            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])
            self.sprites[entity.id].rotation = -90

        def render(self, entity: Entity, window: pyglet.window.Window, position, angle, sprite, **kwargs):
            if entity.id not in self.sprites:
                self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite

            vec = ComponentVector(position)
            newvec = Vector(entity.manager.camera_transform(window, vec.x, vec.y))

            sprite.x, sprite.y = newvec.x, newvec.y
            sprite.scale = 1
            
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



    def get_pos(entity: Entity, component_name: str = 'position') -> ComponentVector:
        assert component_name in entity
        return ComponentVector(entity[component_name])

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
    class S_EditorCursor(System):
        component_types = ['edcursor', 'position', 'shown', 'age', 'cam', 'panspeed']

        def system_init(self):
            self.keyboard = None

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, age, cam, position, panspeed, shown, *args, **kwargs):
            self.keyboard = keyboard

            age.value += dtime
            
            psp = panspeed
            panspeed = panspeed.value * dtime
            
            cam = ComponentVector(cam)
            position = ComponentVector(position)

            if self.keyboard[key.LSHIFT] or self.keyboard[key.RSHIFT]:
                shown.value = False
            
            else:
                shown.value = True

            if keyboard[key.UP]:
                cam.y += panspeed
                position.y += panspeed

            elif keyboard[key.DOWN]:
                cam.y -= panspeed
                position.y -= panspeed

            if keyboard[key.LEFT]:
                cam.x -= panspeed
                position.x -= panspeed

            elif keyboard[key.RIGHT]:
                cam.x += panspeed
                position.x += panspeed

            if keyboard[key.NUM_ADD]:
                psp.value += 10 * dtime

            if keyboard[key.NUM_SUBTRACT]:
                psp.value -= 10 * dtime
                psp.value = max(psp.value, 0)

            entity.manager.set_camera(cam.x, cam.y)
            
        def on_mouse_move(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, position, shown, **kwargs):
            self.mouse_move(entity, window, new_pos, pos_diff, position, shown)

        def on_mouse_drag(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, _, _1, position, shown, **kwargs):
            self.mouse_move(entity, window, new_pos, pos_diff, position, shown)

        def mouse_move(self, entity: Entity, window, new_pos: Vector, pos_diff: Vector, position, shown, **kwargs):
            position = ComponentVector(position)

            nx, ny = entity.manager.un_camera_transform(window, new_pos.x, new_pos.y)

            position.x = nx
            position.y = ny

        def on_mouse_enter(self, entity: Entity, window, xy, shown, **kwargs):
            if self.keyboard and (self.keyboard[key.LSHIFT] or self.keyboard[key.RSHIFT]):
                shown.value = False
            
            else:
                shown.value = True

        def on_mouse_leave(self, entity: Entity, window, xy, shown, **kwargs):
            shown.value = False

        def render(self, entity: Entity, window: pyglet.window.Window, position, shown, age, **kwargs) -> None:
            if shown.value:
                position = ComponentVector(position)
                cx, cy = position.x, position.y

                wx = math.floor(cx / 35) * 35
                wy = math.floor(cy / 35) * 35

                wx, wy = entity.manager.camera_transform(window, wx, wy)

                wx = int(wx)
                wy = int(wy)

                color = (
                    255,
                    255,
                    20,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )
                size = int(35 * self.manager.camera_zoom)

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        # position
                        wx,        wy,
                        wx + size, wy,
                        wx + size, wy + size,
                        wx,        wy + size,
                    )),

                    ('c4B', color * 4)
                )


    @loader.system_type
    class S_Clickables(System):
        component_types = ['clickable', 'position']
        component_defaults = {'down': []}

        def inside(self, mousepos, position, clickable):
            pos = ComponentVector(position)
            cli = ComponentVector(clickable)

            return (
                mousepos.x > pos.x and mousepos.x <= pos.x + cli.x and
                mousepos.y > pos.y and mousepos.y <= pos.y + cli.y
            )

        def on_mouse_press(self, entity, window, pos, button, modifiers, clickable, position, down):
            down = down.value

            if self.inside(pos, position, clickable) and button not in down:
                down.append(button)

            entity['down'] = down

        def on_mouse_release(self, entity, window, pos, button, modifiers, clickable, position, down):
            down = down.value

            if self.inside(pos, position, clickable):
                self.manager.emit(entity, 'click', pos, button, modifiers)

            if button in down:
                down.remove(button)

            entity['down'] = down
        

        def render(self, entity: Entity, window: pyglet.window.Window, down, clickable, position, **kwargs) -> None:
            if down.value:
                position = ComponentVector(position)
                size = ComponentVector(clickable)

                color = (
                    40,
                    40,
                    40,
                    70,
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        # position
                        int(position.x),          int(position.y),
                        int(position.x + size.x), int(position.y),
                        int(position.x + size.x), int(position.y + size.y),
                        int(position.x),          int(position.y + size.y),
                    )),

                    ('c4B', color * 4)
                )


    @loader.system_type
    class S_ObjectPalette(System):
        component_types = ['palette', 'index', 'template', 'selected', 'position', 'age', 'sprite']

        def system_init(self):
            self.selected = None
            self.images = {}
            self.sprites = {}

            for r in self.manager.loader.routines['get.yodine.sprites']:
                self.images.update(r())

        def on_spawned(self, entity: Entity, sprite, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

        def on_loaded(self, entity: Entity, sprite, **kwargs):
            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

        def on_change_sprite(self, entity: Entity, new_sprite, **kwargs):
            if entity.id in self.sprites:
                self.sprites[entity.id].delete()

            self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[new_sprite.value])

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, age, *args, **kwargs):
            age.value += dtime

        def on_resetobjpalselect(self, entity, **kwargs):
            entity['selected'].value = False

        def on_mouse_release(self, entity, window,    xy, button, modifiers,    template, selected,   **kwargs):
            if button & pgmouse.LEFT and (modifiers & pyglet.window.key.MOD_SHIFT):
                self.put(entity, window, xy, template, selected)

        def on_click(self, entity,    xy, button, modifiers,    template, selected,   **kwargs):
            if button & pgmouse.RIGHT:
                self.manager.emit_all('resetobjpalselect')
                entity['selected'].value = True
                self.selected = template.value

        def put(self, entity, window, xy, template, selected):
            if self.selected is not None and selected.value:
                tx, ty = self.manager.un_camera_transform(window, xy.x, xy.y)

                self.manager.create_templated_entity(self.selected, [
                    ('position', [tx, ty])
                ])
        
        def render(self, entity, window,   index, template, selected, position, age, sprite,   **kwargs):
            if entity.id not in self.sprites:
                self.sprites[entity.id] = pyglet.sprite.Sprite(self.images[sprite.value])

            sprite = self.sprites[entity.id] # type: pyglet.sprite.Sprite
                
            wx = 10
            wy = window.height - 40 - index.value * 45

            pos = ComponentVector(position)
            pos.x, pos.y = wx, wy

            wx = int(wx)
            wy = int(wy)

            sprite.x, sprite.y = wx + 35 / 2, wy + 35 / 2
            sprite.scale = 35 / max(sprite.image.width, sprite.image.height)

            if 'scale' in entity:
                scale = entity['scale'].value
                sprite.scale *= scale

            sprite.draw()

            if selected.value:
                color = (
                    60,
                    230,
                    20,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        wx,      wy,
                        wx + 35, wy,
                        wx + 35, wy + 35,
                        wx,      wy + 35,
                    )),
                    ('c4B', color * 4)
                )
            

    @loader.system_type
    class S_TilePalette(System):
        component_types = ['palette', 'index', 'tiletype', 'selected', 'position', 'age']

        def system_init(self):
            self.selected = None

        def tick(self, entity: Entity, dtime: float, keyboard: key.KeyStateHandler, age, *args, **kwargs):
            age.value += dtime

        def on_resetpalselect(self, entity, **kwargs):
            entity['selected'].value = False

        def on_mouse_release(self, entity, window,    xy, button, modifiers,    tiletype, selected,   **kwargs):
            if button & pgmouse.LEFT and not (modifiers & pyglet.window.key.MOD_SHIFT):
                self.put(entity, window, xy, tiletype, selected)

        def on_mouse_drag(self, entity, window,   xy, dxy, button, modifiers,   tiletype, selected,   **kwargs):
            if button & pgmouse.LEFT and not (modifiers & pyglet.window.key.MOD_SHIFT):
                self.put(entity, window, xy, tiletype, selected)

        def on_click(self, entity,    xy, button, modifiers,    tiletype, selected,   **kwargs):
            if button & pgmouse.RIGHT:
                self.manager.emit_all('resetpalselect')
                entity['selected'].value = True
                self.selected = tiletype.value

        def put(self, entity, window, xy, tiletype, selected):
            if self.selected is not None and selected.value:
                tx, ty = self.manager.un_camera_transform(window, xy.x, xy.y)

                tx = math.floor(tx / 35)
                ty = math.floor(ty / 35)

                if self.manager.current_level.tiles[tx, ty] != self.selected:
                    self.manager.current_level.set(Vector((tx, ty)), self.selected)
        
        def render(self, entity, window,   index, tiletype, selected, position, age,   **kwargs):
            wx = window.width - 40
            wy = window.height - 40 - index.value * 45
            entity.manager.force_render_tile(window, tiletype.value, wx, wy)
            position.value = [wx, wy]

            if selected.value:
                color = (
                    20,
                    60,
                    255,
                    int((fast_sin(age.value * math.pi) + 1) * 255 / 2)
                )

                pyglet.graphics.draw(4, pgl.GL_QUADS,
                    ('v2i', (
                        wx,      wy,
                        wx + 35, wy,
                        wx + 35, wy + 35,
                        wx,      wy + 35,
                    )),

                    ('c4B', color * 4)
                )

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

    @loader.routine('preload.Yoded')
    def editor_preinit(game: Editor):
        manag = game.manager
        manag.systems = []

    @loader.routine('postload.Yoded')
    def editor_init(game: Editor):
        manag = game.manager

        for e in manag:
            if 'edcursor' in e or 'palette' in e:
                e.remove()

        manag.create_templated_entity('edcursor', [
            ('cshown', True)
        ])

        for i, tt in enumerate(manag.tile_types.keys()):
            manag.create_templated_entity('edpaletteitem', [
                ('index', i),
                ('tiletype', tt)
            ])

        i = 0
        for tname, template in manag.templates.items():
            if hasattr(template, 'editor_visible') and template.editor_visible:
                manag.create_templated_entity('edobjpalette', [
                    ('index', i),
                    ('sprite', template.get_value('sprite')),
                    ('template', tname)
                ])
                i += 1

        print("Editor initialized successfully.")

def editor_main():
    editor = Editor(os.environ.get('YODINE_GAME', 'yodine_data'), sys.argv[1] if len(sys.argv) > 1 else 'main.save.json')

    if len(sys.argv) > 2:
        lid = sys.argv[2]

        if lid in editor.manager.levels:
            editor.manager.change_level(lid)

        else:
            editor.manager.create_level(lid)

    editor.manager.apply_mod('Yoded', editor_plugin)

    print('Starting Editor...')
    editor.run()


if __name__ == '__main__':
    editor_main()