from distutils.core import setup

setup(
    name='Historical_Data',
    version='0.1.0',
    author='Colin Sav',
    author_email='cjsavacool@gmail.com',
    packages=['OHLCdata'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/Historical_Data/',
    license='LICENSE.txt',
    description='Historical Data collected using TD Ameritrade API',
    long_description=open('README.txt').read(),
    install_requires=[
	"requests == 2.22.0" 
    #    "Django >= 1.1.1",
    #    "caldav == 0.1.4",
    ],
)