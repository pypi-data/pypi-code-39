from gym.envs.registration import register

register(
    id='FrozenIsland-v0',
    entry_point='minigym.envs:FrozenIslandEnv',
)

register(
    id='Platformer-v0',
    entry_point='minigym.envs:PlatformerEnv',
)
