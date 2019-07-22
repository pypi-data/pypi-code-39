import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from minigym.rendering.platformer_viewer import PlatformerViewer

from .core import platformer


class PlatformerEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.scene = None
        self.viewer = None
        self.action_space = spaces.Discrete(6)
        # self.observation_space = ...

    def step(self, action):
        return self.scene.step(action)

    def reset(self):
        self.scene = platformer.scene()
        return self.scene.step(0)[0]

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = PlatformerViewer('minigym:Platformer-v0')

        self.viewer.render(self.scene)

    def close(self):
        self.scene = None
