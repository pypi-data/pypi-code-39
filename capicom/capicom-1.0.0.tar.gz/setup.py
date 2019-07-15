from distutils.core import setup

setup(
    name='capicom',
    version='1.0.0',
    description='Python library to work with CAPICOM',
    author='Rent Dynamics',
    author_email='dev-accounts@rentdynamics.com',
    url='https://github.com/RentDynamics/capicom',
    packages=['capicom'],
    install_requires=[
        'pycrypto',
    ]
)
