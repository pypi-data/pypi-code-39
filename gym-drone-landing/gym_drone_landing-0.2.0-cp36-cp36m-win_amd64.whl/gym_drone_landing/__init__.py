from gym.envs.registration import register

register(
    id='DroneLanding-v0',
    entry_point='gym_drone_landing.envs:DroneLandingEnv',
)
