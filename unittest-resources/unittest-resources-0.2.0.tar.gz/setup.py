# -*- coding: utf-8 -*-
"""
Dynamic resource-based unittest suites made easy.

More details on project `README.md` and
`repository <https://gitlab.com/ergoithz/unittest-resources/>`_.

License
-------
MIT (see LICENSE file).
"""

import io
import re

from setuptools import setup, find_packages

project_url = 'https://gitlab.com/ergoithz/unittest-resources'

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read().replace('](./', '](%s/blob/master/' % project_url)

with io.open('unittest_resources/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='unittest-resources',
    version=version,
    url=project_url,
    license='MIT',
    author='Felipe A. Hernandez',
    author_email='ergoithz@gmail.com',
    description='Dynamic resource-based unittest suites made easy.',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing :: Unit',
        ],
    packages=find_packages(),
    setup_requires=[
        'setuptools>36.2',
        ],
    install_requires=[
        'six',
        'importlib-resources ; python_version<"3.7"',
        ],
    test_suite='unittest_resources.tests',
    tests_require=[
        'pycodestyle',
        'pydocstyle',
        'mypy ; python_version>="3.5"',
        'radon',
        ],
    extras_require={
        'testing': [
            'pycodestyle',
            'pydocstyle',
            'mypy ; python_version>="3.5"',
            'radon',
            ],
        'testing-style': ['pycodestyle', 'pydocstyle'],
        'testing-typing': ['mypy'],
        'testing-maintainability': ['radon'],
        },
    zip_safe=True,
    platforms='any',
    )
