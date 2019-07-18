import time
import os
import pyglet

from typing import Optional, Callable
from .core.entity import Manager, Entity, Component
from .core.vector import Vector
from . import gamedefs
from pyglet.gl import *
from pyglet import clock

try:
    import simplejson as json

except ImportError:
    import json



class Game(object):
    def __init__(self, game_name: str, database_file: Optional[str] = None):
        self.manager = Manager(self) # type: Manager
        self.database_file = database_file # type: Optional[str]
        self.window = pyglet.window.Window()

        gamedefs.load_game(game_name, self)
        self.load(game_name)

        # Enable blending for alpha channel images
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def load(self, init: Callable):
        for e in self.manager:
            e.remove()

        self.manager.levels = {'_DEFAULT': self.manager.default_level}
        
        if self.database_file and os.path.exists(self.database_file):
            with open(self.database_file) as dbfp:
                data = json.load(dbfp)

                for level in data['levels']:
                    level_obj = self.manager.create_level(level['id'])

                    for delta in level['deltas']:
                        level_obj.apply_delta(delta)

                    for entity in level['entities']:
                        level_obj.create_entity(entity['components'], entity['id'])

                for entity in data['entities']:
                    self.manager.create_entity(entity['components'], entity['id'])

                self.manager.change_level(data['currlevel'])

            if not len(self.manager):
                gamedefs.init_game(self)
                self.save()
            
        else:
            gamedefs.init_game(self)
            self.save()

    def save(self):
        if self.database_file:
            with open(self.database_file, 'w') as dbfp:
                data = {
                    'levels': [
                        {
                            'id': l.id,
                            'entities': [
                                {
                                    'components': [(c.name, c.value, type(c).__name__) for c in e],
                                    'id': e.id
                                }
                                for e in l.get_entities()
                            ],
                            'deltas': l.deltas
                        } for l in self.manager.levels.values()
                    ],
                    'entities': [
                        {
                            'components': [(c.name, c.value, type(c).__name__) for c in e],
                            'id': e.id
                        }
                        for e in self.manager.get_entities()
                    ],
                    'currlevel': self.manager.current_level.id
                }

                json.dump(data, dbfp)

    def run(self):
        keyboard = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(keyboard)

        @self.window.event
        def on_draw():
            # render
            self.manager.render(self.window)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, button, mod):
            self.manager.emit_all(('mouse', 'drag'), self.window, Vector((x, y)), Vector((dx, dy)), button, mod)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.manager.emit_all(('mouse', 'move'), self.window, Vector((x, y)), Vector((dx, dy)))

        @self.window.event
        def on_mouse_enter(x, y):
            self.manager.emit_all(('mouse', 'enter'), self.window, Vector((x, y)))

        @self.window.event
        def on_mouse_leave(x, y):
            self.manager.emit_all(('mouse', 'leave'), self.window, Vector((x, y)))

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.manager.emit_all(('mouse', 'press'), self.window, Vector((x, y)), button, modifiers)

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            self.manager.emit_all(('mouse', 'release'), self.window, Vector((x, y)), button, modifiers)

        def tick(dtime):
            # tick
            self.manager.tick(dtime, keyboard)

        clock.schedule_interval(tick, 1 / 60)

        @self.window.event
        def on_close():
            self.save()

        # == keyboard events ==

        try:
            pyglet.app.run()

        except KeyboardInterrupt:
            self.window.close()