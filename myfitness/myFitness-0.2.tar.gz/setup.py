from setuptools import setup, find_packages

setup(
    name='myFitness',
    version='0.2',
    packages=find_packages(exclude=['*test*']),
    license='MIT',
    description='This package provides some basic tools to analyze the health data in a csv file downloaded from Apple Health.',
    url='https://github.com/lizawood/Apple-Health-Fitness-Tracker',
    author='Liza Wood',
    author_email='liza.4.bc@gmail.com'
)
