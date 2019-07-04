from setuptools import setup

setup(
    name='eventmonitoring-client',
    version='1.0',
    py_modules=['hello'],
    install_requires = [
        'requests>=2.18.2',
    ],
)