from setuptools import setup

__version__ = '0.0.1'

setup(
    name='gerridae',
    version=__version__,
    author='buglan',
    description='a crawl framework just for fun',
    author_email='dev.buglan@gmail.com',
    python_requires='>=3.6',
    install_requires=['cssselect', 'lxml', 'requests'],
)