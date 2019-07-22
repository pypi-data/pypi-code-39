import os
import random

import numpy as np
from PIL import Image

from .tiled_renderer import Tiles


class FrozenIslandViewer:
    def __init__(self, title):
        self.viewer = Tiles(500, 500, 64, title, fps=10)
        background_texture = self.viewer.tiles_texture([
            Image.open(os.path.join(__file__, '../assets/frozen_island/background.png')),
        ])
        tiles_texture = self.viewer.tiles_texture([
            Image.open(os.path.join(__file__, '../assets/frozen_island/character.png')),
            Image.open(os.path.join(__file__, '../assets/frozen_island/castle.png')),
            Image.open(os.path.join(__file__, '../assets/frozen_island/tree1.png')),
            Image.open(os.path.join(__file__, '../assets/frozen_island/tree2.png')),
        ])
        self.background = self.viewer.tiles(background_texture, 1)
        self.background.update(np.array([0.0, 0.0, 0.0], 'f4').tobytes())
        self.tiles = self.viewer.tiles(tiles_texture, reserve=65)

    def render(self, env):
        if not self.viewer.wnd.visible:
            return

        rng = random.Random()
        rng.seed(12345)

        data = []
        for row in range(env.nrow):
            for col in range(env.ncol):
                if env.desc[row, col] == b'G':
                    data.append([row - 1.5, 1.5 - col, 1.0])
                elif env.desc[row, col] == b'H':
                    data.append([row - 1.5, 1.5 - col, rng.choice([2.0, 3.0])])

        row, col = env.s // env.ncol, env.s % env.ncol
        data.append([row - 1.5, 1.5 - col, 0.0])

        self.viewer.clear()
        self.background.render()
        self.tiles.update(np.array(data, 'f4').tobytes())
        self.tiles.render()
        self.viewer.flush()
