from distutils.core import setup

requires = ['geocoder', 'pyowm', 'Adafruit_CharLCD', 'RPi.GPIO']

from os import path
with open('README.rst') as f:
    long_description = f.read()
setup(
  name = 'iwPiWeather',
  packages = ['iwPiWeather'],
  version = '0.1.1',
  license = 'gpl-3.0',
  description = 'Gets your weather data for a 16x2 display on raspberry pi',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Dejan Roshkovski',
  url = 'https://github.com/dejanr92/iwPyWeather',
  download_url = 'https://github.com/dejanr92/iwPiWeather/archive/master.zip',
  install_requires=['docutils>=0.3', 'geocoder', 'pyowm', 'Adafruit_CharLCD', 'RPi.GPIO'],
  keywords = ['RaspberryPi', 'LCD display', '16x2', 'Pi'],   # Keywords that define your package best
  package_dir={'iwPiWeather': 'iwPiWeather'},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)