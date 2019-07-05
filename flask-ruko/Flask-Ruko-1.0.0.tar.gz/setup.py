"""
Flask-Ruko
-------------

A Flask extension to connect to a Ruko database
"""
from setuptools import setup


setup(
    name='Flask-Ruko',
    version='1.0.0',
    url='https://github.com/rukodb/flask-ruko',
    license='MIT',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    description='A Flask extension to connect to a Ruko database',
    long_description=__doc__,
    py_modules=['flask_ruko'],
    install_requires=[
        'Flask',
        'werkzeug',
        'ruko'
    ],
    keywords='ruko database in-memory',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',

        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)

