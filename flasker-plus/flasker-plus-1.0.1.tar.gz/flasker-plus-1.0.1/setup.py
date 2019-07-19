
from setuptools import setup

setup(
    name='flasker-plus',
    author='Connor Mullett',
    install_requires=[
        'Click'
    ],
    version='1.0.1',
    entry_points={
        'console_scripts': [
            'flaskerplus=flasker_plus.main:main',
        ]
    }
)

