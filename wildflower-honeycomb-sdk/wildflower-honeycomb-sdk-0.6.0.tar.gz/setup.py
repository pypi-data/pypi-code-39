import os
from setuptools import setup, find_packages

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VERSION = open(os.path.join(BASEDIR, 'VERSION')).read().strip()
REQUIREMENTS = []


with open(os.path.join(BASEDIR, 'requirements.pip')) as fp:
    lines = fp.readlines()
    for line in lines:
        line = line.strip()
        REQUIREMENTS.append(line)

# allow setup.py to be run from any path
os.chdir(os.path.normpath(BASEDIR))


setup(
    name='wildflower-honeycomb-sdk',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    description='SDK for use with the Wildflower Honeycomb API',
    long_description='Provides uniform access to all aspects of the honeycomb API as well as a direct GraphQL interface for more complex queries.',
    url='https://github.com/Wildflowerschools/py-honeycomb-sdk',
    author='optimuspaul',
    author_email='paul.decoursey@wildflowerschools.org',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'honeycomb=cli:cli',
        ],
    }
)
