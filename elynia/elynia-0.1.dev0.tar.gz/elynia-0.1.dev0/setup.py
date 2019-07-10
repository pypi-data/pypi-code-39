from setuptools import setup, find_packages

setup(
    name='elynia',
    version='0.1dev',
    description='A re-write of Monica, a cli-based food recommendation service',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
)