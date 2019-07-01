import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel('intezer_sdk', '__init__.py'), 'r') as f:
    version_marker = '__version__ = '
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip("'")
            break
    else:
        raise RuntimeError('Version marker not found.')

install_requires = [
    'requests >= 2.21.0,<3',
    'enum34==1.1.6 ; python_version < "3.0"'
]
setup(
    name='intezer_sdk',
    version=version,
    packages=['intezer_sdk'],
    url='',
    license='Apache License v2',
    author='Intezer Labs ltd.',
    author_email='info@intezer.com',
    description='Intezer Analyze SDK',
    install_requires=install_requires,
    keywords='intezer',
    test_requires=[
        'responses == 0.10.5',
        'pytest == 3.6.4',
        'mock == 2.0.0'
    ],
    python_requires='>=3.5',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
