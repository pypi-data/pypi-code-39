from setuptools import setup

setup(
    name='curl_modifier',
    version='1',
    packages=['curl_modifier'],
    url='https://github.com/Zenulous/curl_modifier',
    author='Zen van Riel',
    author_email='zenvanriel@gmail.com',
    description='A module for modifying and repeatedly executing cURL requests',
    install_requires=['requests', 'uncurl'],
)
