from setuptools import setup, find_packages
from cnvrg.version import VERSION
setup(
    name='cnvrg',
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        'click', 'requests', "boto3", 'colorama', "tqdm", "pyaml", 'tinynetrc', 'pycrypto'
    ],
    author="cnvrg",
    author_email="support@cnvrg.io",
    entry_points='''
        [console_scripts]
        cnvrgp=cnvrg.main:cli
    ''',
)