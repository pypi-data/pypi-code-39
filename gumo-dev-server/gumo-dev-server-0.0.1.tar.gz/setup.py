import setuptools


name = 'gumo-dev-server'
version = '0.0.1'
description = 'Gumo Dev Server Utilities'
dependencies = [
    'pyyaml >= 5.1',
    'injector >= 0.13.1',
    'gumo-core >= 0.1.0',
    'gumo-task-emulator >= 0.1.0',
    'datastore-viewer >= 0.0.6'
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
            'gumo-dev-server = gumo.dev_server:gumo_dev_server',
        ]
    },
    include_package_data=True,
)
