"""
Setup.py for notifybot
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='notifybot3',
    version='0.0.5',
    description='Slack Notifications for Travis Deploys',
    long_description='A CLI to notify Slack on Travis CI deployments by API token or Incoming Webhook URL',
    url='https://github.com/chuckoy/notifybot',
    author='Daniel Whatmuff',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='travis deployment slack notification',
    py_modules=["notifybot3"],
    install_requires=[
        'slackclient~=2.1.0',
        'requests~=2.14.0',
    ],
    scripts=['bin/notifybot'],
)
