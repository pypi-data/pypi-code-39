from setuptools import setup, find_packages

__version__ = '0.0.2'

setup(
    name='gerridae',
    version=__version__,
    author='buglan',
    packages=find_packages(),
    description='a crawl framework just for fun',
    author_email='dev.buglan@gmail.com',
    python_requires='>=3.6',
    install_requires=['cssselect', 'lxml', 'requests'],
)
