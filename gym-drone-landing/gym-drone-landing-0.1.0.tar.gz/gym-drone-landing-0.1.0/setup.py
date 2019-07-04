from setuptools import Extension, setup

ext = Extension(
    name='gym_drone_landing.core',
    sources=['gym_drone_landing/core/core.cpp'],
)

setup(
    name='gym-drone-landing',
    version='0.1.0',
    ext_modules=[ext],
)
