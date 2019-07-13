from setuptools import setup

setup(  name='chikfactor',
        version='1.0',
        description='Calculate K-factor for EM production of chi in NRQCD',
        packages=['chikfactor'],
        author='Daniel Mueller',
        author_email='xdaniel.muellerx@gmx.de',
        license='MIT',
        zip_safe=False,
        url='https://github.com/SchneePingu/chikfactor',
        install_requires=['mpmath'] )
