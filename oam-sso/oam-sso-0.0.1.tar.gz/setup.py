from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'beautifulsoup4==4.7.1',
    'certifi==2019.6.16',
    'chardet==3.0.4',
    'idna==2.8',
    'requests==2.22.0',
    'soupsieve==1.9.2',
    'urllib3==1.25.3'
]

setup(
    name='oam-sso',
    version='0.0.1',
    packages=['oam_sso'],
    install_requires=requires,
    url='https://github.com/mtucker502/oam-sso',
    license='MIT License',
    author='mtucker502',
    author_email='github@netzolt.com',
    description='Easily access pages protected with Oracle Access Management SSO',
    long_description=long_description
)
