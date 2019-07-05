from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='meraki-sdk',
    version='1.0.0',
    description='Python client library for Meraki Dashboard API'.encode("utf-8").decode(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='APIMatic SDK Generator',
    author_email='support@apimatic.io',
    url='https://create.meraki.io',
    packages=find_packages(),
    install_requires=[
        'requests>=2.9.1, <3.0',
        'jsonpickle>=0.7.1, <1.0',
        'cachecontrol>=0.11.7, <1.0',
        'python-dateutil>=2.5.3, <3.0'
    ]
)