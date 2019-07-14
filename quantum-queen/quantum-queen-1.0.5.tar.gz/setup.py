#!/usr/bin/env python3
from setuptools import find_packages
from setuptools import setup


REQUIREMENTS = [
    'ansible==2.8.1',
    'requests==2.22.0'
]


setup(
    name='quantum-queen',
    version='1.0.5',
    project_name='Quantum Queen',
    author='Cochise Ruhulessin',
    author_email='cochise.ruhulessin@wizardsofindustry.com',
    url='https://www.wizardsofindustry.com',
    description='Unimatrix One Provisioning Library (Quantum Queen)',
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True
)
