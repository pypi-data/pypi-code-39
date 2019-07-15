from setuptools import setup, find_packages
import sys


def is_python3():
    if (sys.version[0] == '3'):
        return True
    else:
        return False
		
if is_python3(): 
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
else:
    with open('README.md', 'r') as fh:
        long_description = fh.read()


setup(
    name='bc_dock_util',
    version='0.1.0',
    author='caifh',
    author_email='caifh@tianxiaxinyong.com',
    description='B client docking tianxiaxinyong service sdk util.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/pytxxy/bc_dock_util',
    install_requires=[
        'pycryptodome>=3.5.1',
        'cryptography>=2.3',
        'Requests>=2.19.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
