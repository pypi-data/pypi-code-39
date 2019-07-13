from distutils.core import setup

setup(
    name='DegreePlaner',
    version='1.3.0',
    author='Vladimir Parakhin',
    author_email='vov4ikpa@gmail.com',
    packages=['towelstuff', 'towelstuff.test'],
    scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/DegreePlaner/',
    license='LICENSE.txt',
    description='Technion degree planer',
    long_description=open('README.txt').read(),
    install_requires=[
        "bs4 >= 1.1.1",
        "requests == 0.1.4",
        "PyQt5",
        "html5",
        "lxml"
    ],
)