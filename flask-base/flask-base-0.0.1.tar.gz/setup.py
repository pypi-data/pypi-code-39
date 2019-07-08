# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from collections import OrderedDict

version = "0.0.1"

readme = ''
with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='flask-base',
    version=version,
    description='A simple Flask boilerplate app with SQLAlchemy, Redis, User Authentication, and more.',
    long_description=readme,
    url='https://github.com/longniao/flask-base',
    keywords='flask-base flask',
    author='Longniao',
    author_email='longniao@gmail.com',
    maintainer='Longniao',
    maintainer_email='longniao@gmail.com',
    license='MIT',
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'alembic',
        'appdirs',
        'blinker',
        'click',
        'Faker',
        'Flask',
        'Flask-Assets',
        'Flask-Compress',
        'Flask-Login',
        'Flask-Mail',
        'Flask-Migrate',
        'Flask-RQ',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'Flask-SSLify',
        'Flask-WTF',
        'gunicorn',
        'honcho',
        'itsdangerous',
        'Jinja2',
        'jsmin',
        'jsonpickle',
        'Mako',
        'MarkupSafe',
        'packaging',
        'psycopg2',
        'pyparsing',
        'python-dateutil',
        'python-editor',
        'raygun4py',
        'redis',
        'requests',
        'rq',
        'six',
        'SQLAlchemy',
        'webassets',
        'Werkzeug',
        'WTForms',
    ])
