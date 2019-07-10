from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyrgbpalette',
    version='0.0.6',
    description='Generate rgb palette in red or rainbow',
    py_modules=["rgbpalette"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [
    ],
    extras_require = {
        "dev": [
           "ddt>=1.2",
           "twine>=1.13"
        ],
    },
    url="https://github.com/myplaceit/pyrgbpalette",
    author="Wolfgang Hoellinger",
    author_email="wolfgang.hoellinger@myplace.eu",
)