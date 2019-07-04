"""A setuptools-based setup module for a Python package.

See:
https://setuptools.readthedocs.io/en/latest/setuptools.html
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


import io
import re
from os import path
from setuptools import setup, find_packages

import znbstatic

packages = find_packages()

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, 'README.rst'), 'rt', encoding='utf8') as f:
    readme = f.read()

# a more complicated alternative to getting version, replace it in setup call below.
# with io.open(path.join(here, 'znbstatic/__init__.py'), 'rt', encoding='utf8') as f:
#     version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='znbstatic',
    version=znbstatic.__version__,
    python_requires='>=3',
    install_requires=[
        'Django>=2.0',
        'boto3>=1.9.70,<2',
        'django-storages>=1.7.1,<2',
    ],
    author='Alexis Bellido',
    author_email='a@zinibu.com',
    license='BSD, see LICENSE file',
    description='A Django storage backend with versioning and S3 support.',
    long_description=readme,
    long_description_content_type='text/x-rst',
    url="https://github.com/alexisbellido/znbstatic",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    package_dir={'znbstatic': 'znbstatic'},
    package_data={'': ['README.rst', 'LICENSE']},
    include_package_data=True
)
