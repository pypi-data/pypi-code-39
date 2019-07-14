import setuptools


name = 'gumo-dev-server'
version = '0.0.1a3'
description = 'Gumo Dev Server Utilities'
dependencies = [
    'pyyaml >= 5.1',
    'injector >= 0.13.1',
    'gumo-core >= 0.1.0a7',
    'gumo-task-emulator >= 0.1.0a3',
    'datastore-viewer >= 0.0.6a0'
]

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = [
    package for package in setuptools.find_packages()
    if package.startswith('gumo')
]

setuptools.setup(
    name=name,
    version=version,
    author="Gumo Project Team",
    author_email="gumo-py@googlegroups.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gumo-py/gumo-dev-server",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'gumo-dev-server = gumo.core:gumo_dev_server',
        ]
    },
)
