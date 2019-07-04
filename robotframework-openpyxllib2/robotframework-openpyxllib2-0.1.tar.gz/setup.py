from setuptools import setup, find_packages

with open("README.txt", "r") as fh:
	long_description = fh.read()

setup(

    name='robotframework-openpyxllib2',
    version='0.1',
    description='Robotframework library for excel xlsx file format',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/matthewdy/robotframework-openpyxllib',
    author='Vallinayagam.K',
    author_email='yuemoon2006@hotmail.com',
    packages=find_packages(),
    install_requires=['openpyxl']
    
)
