import time
import traceback
import random
import trio
import os
import pyglet

from typing import Optional, Callable, Tuple
from .core.entity import Manager, Entity, Component
from .core.vector import Vector
from .core.network import Client, Server
from . import gamedefs
from pyglet.gl import *
from pyglet import clock

try:
    import simplejson as json

except ImportError:
    import json



class EventLoop(object):
    def __init__(self, window):
        self.window = window
        self.stop()

    def run(self):
        trio.run(self.async_run)

    def stop(self):
        self.running = False

    async def async_run(self):
        self.running = True

        while self.running:
            clock.tick()

            self.window.switch_to()
            self.window.dispatch_events()
            self.window.dispatch_event('on_draw')
            self.window.flip()

            await trio.sleep(0)

        self.window.close()


class Game(object):
    def __init__(self, game_name: str, database_file: Optional[str] = None):
        self.window = pyglet.window.Window()
        self.manager = Manager(self, self.window) # type: Manager
        self.database_file = database_file # type: Optional[str]

        gamedefs.load_game(game_name, self)
        self.load(game_name)
        self.event_loop = EventLoop(self.window)

        # Enable blending for alpha channel images
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def stop(self):
        self.event_loop.stop()

    async def loop(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.event_loop.async_run)

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
                self.manager.emit_all('loaded')
            
        else:
            gamedefs.init_game(self)
            self.save()

    def save(self):
        if self.database_file:
            self.manager.emit_all('saved')

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

    def on_draw(self):
        self.manager.render(self.window)

    def on_mouse_drag(self, x, y, dx, dy, button, mod):
        self.manager.emit_all(('mouse', 'drag'), self.window, Vector((x, y)), Vector((dx, dy)), button, mod)

    def on_mouse_motion(self, x, y, dx, dy):
        self.manager.emit_all(('mouse', 'move'), self.window, Vector((x, y)), Vector((dx, dy)))

    def on_mouse_enter(self, x, y):
        self.manager.emit_all(('mouse', 'enter'), self.window, Vector((x, y)))

    def on_mouse_leave(self, x, y):
        self.manager.emit_all(('mouse', 'leave'), self.window, Vector((x, y)))

    def on_mouse_press(self, x, y, button, modifiers):
        self.manager.emit_all(('mouse', 'press'), self.window, Vector((x, y)), button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.manager.emit_all(('mouse', 'release'), self.window, Vector((x, y)), button, modifiers)

    def on_close(self):
        self.save()
        self.stop()

    def run(self):
        keyboard = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(keyboard)
        self.window.push_handlers(self)

        def tick(dtime):
            # tick
            self.manager.tick(dtime, keyboard)

        clock.schedule_interval(tick, 1 / 60)

        # == keyboard events ==

        try:
            trio.run(self.loop)

        except KeyboardInterrupt:
            self.window.close()
            traceback.print_exc()