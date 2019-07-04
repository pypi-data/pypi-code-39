#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (3, 4):
    raise NotImplementedError("Sorry, you need at least Python 3.4 TinCan.")

setup(name='TinCanFramework',
      version='0.1.0',
      description='Simple code-behind WSGI framework for small web-applications, implemented on top of bottle.',
      author="David W. Barts",
      author_email="tincan@bartsent.com",
      url='http://bartsent.com/tincan.pspx',
      py_modules=['tincan'],
      scripts=['bin/install-static', 'bin/launch'],
      license='MIT',
      platforms='any',
      install_requires=['bottle>=0.12.0'],
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   ],
      )

