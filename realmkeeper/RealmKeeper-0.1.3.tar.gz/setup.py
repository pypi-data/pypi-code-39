import re
from setuptools import setup
import os

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('realmkeeper/realmkeeper.py').read(),
    re.M
    ).group(1)


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='RealmKeeper',
    packages=['realmkeeper'],
    entry_points={
        'console_scripts': ['realmkeeper = realmkeeper.realmkeeper:main']
        },
    version=version,
    description='Python Utility to manage hosts with FreeIPA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jake Neyer',
    author_email='jaken551@gmail.com',
    install_requires=['Flask==0.12.2',
                      'python-freeipa==0.2.3',
                      'boto3 == 1.9.180',
                      'botocore == 1.12.180',
                      'pyOpenSSL == 19.0.0']
    )
