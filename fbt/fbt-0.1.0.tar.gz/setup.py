#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

package_name = "fbt"
package_version = "0.1.0"
description = """Fork of dbt-presto for a custom build stack"""

setup(
    name=package_name,
    version=package_version,
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/tjwaterman99/fbt',
    packages=find_packages(),
    package_data={
        'dbt': [
            'include/presto/dbt_project.yml',
            'include/presto/macros/*.sql',
            'include/presto/macros/*/*.sql',
        ]
    },
    install_requires=[
        'dbt-core==0.13.1',
        'presto-python-client',
    ]
)
