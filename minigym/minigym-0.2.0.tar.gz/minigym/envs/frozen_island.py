import gym

from minigym.rendering.frozen_island_viewer import FrozenIslandViewer


class FrozenIslandEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.viewer = None
        self.env = gym.make('FrozenLake-v0')
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human'):
        if self.viewer is None:
            self.viewer = FrozenIslandViewer('minigym:FrozenIsland-v0')

        self.viewer.render(self.env)

    def close(self):
        self.env.close()
