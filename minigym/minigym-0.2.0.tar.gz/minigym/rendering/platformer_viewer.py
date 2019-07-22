import os
import random

import numpy as np
from PIL import Image

from .tiled_renderer import Tiles


class PlatformerViewer:
    def __init__(self, title):
        self.viewer = Tiles(600, 400, 64, title, fps=60)
        background_texture = self.viewer.tiles_texture([
            Image.open(os.path.join(__file__, '../assets/platformer/background.png')),
        ])
        character_texture = self.viewer.tiles_texture([
            Image.open(os.path.join(__file__, '../assets/platformer/idle_right.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/idle_left.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/walk_right1.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/walk_right2.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/walk_left1.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/walk_left2.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/jump_right.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/jump_left.png')),
        ])
        tiles_texture = self.viewer.tiles_texture([
            Image.open(os.path.join(__file__, '../assets/platformer/grass.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/bush.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/closed_door1.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/closed_door2.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/open_door1.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/open_door2.png')),
            Image.open(os.path.join(__file__, '../assets/platformer/key.png')),
        ])
        self.background = self.viewer.tiles(background_texture, 1)
        self.background.update(np.array([0.0, 0.0, 0.0], 'f4').tobytes())
        self.character = self.viewer.tiles(character_texture, 1)
        self.static_tiles = self.viewer.tiles(tiles_texture, reserve=16)
        self.progress0 = self.viewer.tiles(tiles_texture, reserve=8)
        self.progress1 = self.viewer.tiles(tiles_texture, reserve=8)
        self.static_tiles.update(np.array([
            -3.5, -2.5, 0.0,
            -2.5, -2.5, 0.0,
            -1.5, -2.5, 0.0,
            -0.5, -2.5, 0.0,
            0.5, -2.5, 0.0,
            1.5, -2.5, 0.0,
            2.5, -2.5, 0.0,
            3.5, -2.5, 0.0,
            1.5, 0.5, 0.0,
            2.5, 0.5, 0.0,
            3.5, 0.5, 0.0,
            -2.5, -1.5, 1.0,
        ], 'f4').tobytes())
        self.progress0.update(np.array([
            3.5, 1.5, 2.0,
            3.5, 2.5, 3.0,
            -3.5, -1.5, 6.0,
        ], 'f4').tobytes())
        self.progress1.update(np.array([
            3.5, 1.5, 4.0,
            3.5, 2.5, 5.0,
        ], 'f4').tobytes())

    def render(self, scene):
        if not self.viewer.wnd.visible:
            return

        for state, progress in scene.frames():
            self.viewer.clear()
            self.background.render()
            self.static_tiles.render()
            if progress == 0:
                self.progress0.render()
            if progress != 0:
                self.progress1.render()
            if progress != 2:
                self.character.update(np.array(state, 'f4').tobytes())
                self.character.render()
            self.viewer.flush()
