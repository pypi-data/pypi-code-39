#!/usr/bin/env python

from distutils.core import setup

# This setup is suitable for "python setup.py develop"

# Work around mbcs bug in distutils. 
# http://bugs.python.org/issue10945
import codecs 
try: 
    codecs.lookup('mbcs') 
except LookupError: 
    ascii = codecs.lookup('ascii') 
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs') 
    codecs.register(func) 

setup(name='mymath_stupid',
	version='0.1',
	description='A stupid math package',
	author='Fandi Iksani',
	author_email='iksani.f@gmail.com',
	url='http://sillymath.workd.id',
	packages=['mymath_stupid', 'mymath_stupid.adv'])