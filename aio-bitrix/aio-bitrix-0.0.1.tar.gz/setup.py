from io import open
from setuptools import setup, find_packages

def read(f):
    return open(f, 'r', encoding='utf-8').read()

setup(
    name='aio-bitrix',
    version='0.0.1',
    packages=find_packages(),
    description='Async Wrapper for Bitrix24 REST API',
    # long_description=read('README.md'),
    author='bzdvdn',
    author_email='bzdv.dn@gmail.com',
    url='https://github.com/bzdvdn/aio_bitrix/',
    license='MIT',
    python_requires=">=3.6",
    install_requires = [
        'aiohttp==3.4.4',
    ]
    
)
