#
# Copyright (c) 2019, Prometheus Research, LLC
#

from setuptools import setup, find_packages

setup(
    name='htsql_xport',
    version='0.1.1',
    description='An HTSQL extension that adds basic SAS V5 XPORT transport file support.',
    long_description=open('README.rst', 'r').read(),
    author='Prometheus Research, LLC',
    license='AGPLv3',
    url='https://bitbucket.org/prometheus/htsql_xport',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    entry_points={
        'htsql.addons': [
            'htsql_xport = htsql_xport:XPTAddon',
        ],
    },
    install_requires=[
        'HTSQL>=2.3,<3',
        'xport==2.0.2',
    ],
)
