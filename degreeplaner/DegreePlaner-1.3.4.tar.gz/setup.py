from distutils.core import setup

setup(
    name='DegreePlaner',
    version='1.3.4',
    author='Vladimir Parakhin',
    author_email='vov4ikpa@gmail.com',
    packages=['degreeplaner'],
    include_package_data=True,
    url='http://pypi.python.org/pypi/DegreePlaner/',
    license='LICENSE.txt',
    description='Technion degree planer',
    long_description=open('README.txt').read(),
    install_requires=[
        "bs4",
        "requests",
        "PyQt5",
        "html5",
        "lxml"
    ],
)