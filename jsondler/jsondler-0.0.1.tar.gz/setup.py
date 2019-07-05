from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jsondler',
    version='0.0.1',
    author="Denis Moshensky",
    author_email="loven7doo@gmail.com",  
    description="JSON handler for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loven-doo/jsondler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={},
    install_requires=[
        'numpy >= 1.15.1',
        'pandas >= 0.23.4',
    ],
    entry_points={
        'console_scripts': []
    }
)
