from distutils.core import setup
setup(
name='flb',
version='1.1',
author='Nasir Ali',
author_email='nasiralis1731@gmail.com',
author_url='https://facebook.com/nasir.xo',
packages=['flb'],
scripts=['bin/flb'],
install_requires=['bs4','requests', ],
)
