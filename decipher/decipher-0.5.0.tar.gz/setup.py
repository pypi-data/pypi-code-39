from distutils.core import setup

setup(
    name='decipher',
    version='0.5.0',
    description="Package for easier access to Decipher's Beacon REST API",
    author='Erwin S. Andreasen',
    long_description=open('README.rst').read(),
    author_email='beacon-api@decipherinc.com',
    url='https://www.decipherinc.com/n/',
    packages=['decipher'],
    license="BSD",
    requires=["requests"],
    scripts=['scripts/beacon']
)
