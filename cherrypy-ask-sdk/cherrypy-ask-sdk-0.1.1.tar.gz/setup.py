import setuptools
from setuptools.config import read_configuration

config = read_configuration("setup.cfg")
setup_params = {}
setup_params = dict(setup_params, **config['metadata'])
setup_params = dict(setup_params, **config['options'])
# at this point there is not a simpler way to load a requires file
# directly from the setup.cfg file
setup_params['install_requires'] = [
    line.strip() for line in open("requires.txt").read().splitlines()
]
setuptools.setup(**setup_params)
