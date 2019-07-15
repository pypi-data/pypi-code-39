from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read()

setup(
        name='xylem-daq',
        version=version,
        description='Modular DAQ system',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/samkohn/xylem',
        author='Sam Kohn',
        author_email='skohn@lbl.gov',
        keywords='daq physics',
        packages=find_packages(),
        install_requires=['pyzmq', 'eventlet >= 0.24']
)
