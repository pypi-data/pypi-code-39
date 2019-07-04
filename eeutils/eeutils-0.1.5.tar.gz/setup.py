# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


with open("eeutils/_version.py", "r") as version_file:
    version_content = version_file.read()
    exec(version_content)


install_requires = [
    'Click',
    'click-completion',
    'colorama',
    'psycopg2',
    'psycopg2-binary',
    'terminaltables',
    'polib',
    'googletrans',
]

setup(
    name='eeutils',
    # Version fetched from eeutils/_version.py (Change only there please)
    version=globals().get('__version__'),
    description='Utility commands for Development',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.e-mips.com.ar/infra/eeutils',
    author='Martín Nicolás Cuesta/Santiago Said',
    author_email='cuesta.martin.n@hotmail.com',
    maintainer="Eynes & E-MIPS",
    maintainer_email="cuesta.martin.n@hotmail.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license='AGPL3+',
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    zip_safe=False,
    entry_points='''
        [console_scripts]
        eeutils=eeutils.main:eeutils
        eebash=eeutils.main:bash
        eeodoo=eeutils.main:odoo
        eegit=eeutils.main:git
    ''',
)
