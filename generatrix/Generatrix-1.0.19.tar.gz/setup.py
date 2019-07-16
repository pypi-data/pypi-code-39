from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Generatrix',
    version='1.0.19',
    author='Fernando A. Balandran',
    author_email='fredz0003@gmail.com',
    description='Generates repo contents markdown',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/kodaman2/generatrix_py',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    entry_points={
        'console_scripts': [
            'gtrix = generatrix_py.generatrix:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)