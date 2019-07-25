from setuptools import setup

LOCAL_PACKAGE_DIRECTORY_NAMES = ['lib', 'lib.commands']
MODULES = ['index']
CONSOLE_SCRIPTS = ['macroscope=index:cli']

# dependencies
REQUIRED_DEPENDENCIES = [
        'click',
        'numpy',
        'sklearn',
        'pandas',
        'matplotlib',
        'networkx',
        'community',
        'python-louvain'
    ]
DEV_DEPENDENCIES = ['wheel', 'flake8', 'autopep8']

setup(
    name='macroscope',
    # TODO: Automate version number changes - django has an example in their setup.py
    version='0.0.10',
    author='StraightOuttaCrompton',
    author_email='soc@email.com',
    description='The macroscope command line interface',
    packages=LOCAL_PACKAGE_DIRECTORY_NAMES,
    py_modules=MODULES,
    install_requires=REQUIRED_DEPENDENCIES,
    extras_require={
        'dev': DEV_DEPENDENCIES
    },
    # TODO: get this project to run with python 2 if possible
    python_requires='>=3.0.*',
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS
    }
)
