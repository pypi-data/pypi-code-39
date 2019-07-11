import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyIndego",
    version="0.0.6",
    author="Jens Mazzanti-Myretyr",
    author_email="jens@myretyr.se",
    description="API for Bosch Indego mower",
    long_description="API for Bosch Indego mower",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)