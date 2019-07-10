from setuptools import find_packages, setup

import os
import re


def get_version():
    with open(os.path.join(os.path.dirname(__file__), 'pgcrypto', 'base.py')) as fp:
        return re.match(r".*__version__ = '(.*?)'", fp.read(), re.S).group(1)

setup(
    name='django-pgcrypto2',
    version=get_version(),
    description='Python and Django utilities for encrypted fields using pgcrypto.',
    author='Dan Watson & Fran Lendinez',
    author_email='dcwatson@gmail.com',
    url='https://github.com/dcwatson/django-pgcrypto',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'pycryptodome==3.8.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
    ]
)
