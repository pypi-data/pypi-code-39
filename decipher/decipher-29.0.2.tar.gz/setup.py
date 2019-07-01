from distutils.core import setup

setup(
    name='decipher',
    version='29.0.2',
    description="Package for easier access to FocusVision's Decipher REST API",
    author='Erwin S. Andreasen',
    long_description=open('README.rst').read(),
    author_email='beacon-api@decipherinc.com',
    url='https://www.focusvision.com/products/decipher/',
    packages=['decipher', 'decipher.commands'],
    license="BSD",
    requires=["requests"],
    scripts=['scripts/beacon']
)
