from setuptools import setup, find_packages

setup(
    name="py-iaso",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
        'docker',
        'sendgrid',
    ],
	entry_points={
        'console_scripts': [
            'iaso = pyiaso.main:run',
        ],
    },
)